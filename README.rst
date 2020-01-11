SecretsLibrary
================
A Robot Framework library to help with secrets management

Why I wrote this:

::

    During my time trying to get my codebase and my AT working together, I encountered some scenarios:

        * Where do I keep credentials for access to databases, servers, etc?
        * How can I save these credentials safely with my codebase?

After some time playing around with Bamboo Secrets and GitHub Encrypted Secrets, I decided to rationalise the inputs to
a single decryption key and store all my secrets in a file in the repository itself.

Seeing that Python has great crypto libraries already at it's disposal, it was a trivial task to implement them in
Robot as keywords, and thus this project was created.

The library offers Asymmetric and Symmetric encryption/decryption. In fact, if you use both together you get the
ability to digitally sign your data!

In the future I plan to integrate this with more secret keeps (Hashicorp Vault, Azure KeyVault, etc)
