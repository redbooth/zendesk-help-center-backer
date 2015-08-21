"""
Setup computer for editing the help center website.
"""

import subprocess

# Install watchdog for tracking changes in a directory.
subprocess.call("pip install watchdog", shell = True)

# Install boto for using Amazon's CloudFront.
subprocess.call("pip install boto", shell = True)

# Install colorama for colored errors and warnings.
subprocess.call("pip install colorama", shell = True)

# Install zdesk for zdesk API usage.
subprocess.call("pip install zdesk", shell = True)
