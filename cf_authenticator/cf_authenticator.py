import json
import os
import urllib.request
import jwt
from jupyterhub.auth import Authenticator
from traitlets import Unicode, default
import logging

# Create a logger specific to this module
logger = logging.getLogger(__name__)

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class CFAuthenticator(Authenticator):
    """
    JupyterHub authenticator for Cloudflare Access that validates JWT tokens.
    
    This authenticator integrates with Cloudflare Access to provide secure authentication
    for JupyterHub. It validates JWT tokens issued by Cloudflare Access and uses the
    email address from the token as the username for JupyterHub sessions.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set expected audience and team domain from environment variables
        self.policy_aud = os.getenv("POLICY_AUD")
        self.team_domain = os.getenv("TEAM_DOMAIN")
        
        if not self.policy_aud or not self.team_domain:
            raise ValueError("POLICY_AUD and TEAM_DOMAIN environment variables must be set")
            
        self.certs_url = f"{self.team_domain}/cdn-cgi/access/certs"
        self.identity_url = f"{self.team_domain}/cdn-cgi/access/get-identity"
        logger.info(f"Initialized CFAuthenticator with team domain: {self.team_domain}")

    @default("auto_login")
    def _auto_login_default(self):
        """Enable automatic login by default."""
        return True

    def get_public_keys(self):
        """
        Fetch and parse Cloudflare's public signing keys.
        
        Returns:
            list: List of RSA public key objects used for JWT validation
        
        Raises:
            URLError: If unable to fetch the public keys
            JSONDecodeError: If the response is not valid JSON
        """
        try:
            with urllib.request.urlopen(self.certs_url) as response:
                jwk_set = json.load(response)
                public_keys = [
                    jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
                    for key in jwk_set['keys']
                ]
                logger.debug(f"Successfully fetched {len(public_keys)} public keys")
                return public_keys
        except Exception as e:
            logger.error(f"Error fetching public keys: {str(e)}")
            raise

    async def authenticate(self, handler, data=None):
        """
        Authenticate user by validating the Cloudflare Access JWT token.
        
        Args:
            handler: The request handler
            data: Additional data (not used)
            
        Returns:
            dict: User information including name (email)
            
        Raises:
            Exception: If token is missing, invalid, or authentication fails
        """
        logger.debug(f"Headers: {json.dumps(dict(handler.request.headers))}")
        
        token = handler.request.headers.get("cf-access-jwt-assertion")
        if not token:
            logger.error("Missing Cloudflare JWT token")
            raise Exception("Missing Cloudflare JWT token")

        public_keys = self.get_public_keys()
        email = None

        for key in public_keys:
            try:
                decoded_token = jwt.decode(
                    token,
                    key=key,
                    audience=self.policy_aud,
                    algorithms=["RS256"]
                )
                logger.debug(f"Decoded token: {json.dumps(decoded_token, indent=4)}")
                email = decoded_token.get("email")
                if email:
                    break
            except jwt.ExpiredSignatureError:
                logger.error("Token has expired")
                raise Exception("Token has expired")
            except jwt.InvalidTokenError:
                continue

        if not email:
            logger.error("Invalid token or email claim missing")
            raise Exception("Invalid token or email claim missing")

        # Fetch identity details
        try:
            identity_request = urllib.request.Request(self.identity_url)
            identity_request.add_header("cookie", f"CF_Authorization={token}")
            
            with urllib.request.urlopen(identity_request) as identity_response:
                identity_data = json.load(identity_response)
                logger.debug(f"Identity data: {json.dumps(identity_data, indent=4)}")
                
            logger.info(f"Successfully authenticated user: {email}")
            return {"name": email}
            
        except Exception as e:
            logger.error(f"Error fetching identity data: {str(e)}")
            raise Exception(f"Failed to fetch identity data: {str(e)}")
