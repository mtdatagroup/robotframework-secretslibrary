*** Settings ***

Resource                            resources/common.robot

Test Setup                          Configure Engines
Default Tags                        Secrets

*** Test Cases ***
Test Symmetric
    Switch Engine                   Fernet
    ${plain_text}=                  Get File                    ${SAMPLE_PLAIN_TEXT}
    ${encrypted}=                   Encrypt                     ${plain_text}
    Should not be Equal as Strings  ${encrypted}                ${plain_text}
    ${decrypted}=                   Decrypt                     ${encrypted}
    Should be Equal as Strings      ${decrypted}                ${plain_text}
    Should not be Equal as Strings  ${encrypted}                ${decrypted}

Test Symmetric file keywords
    Switch Engine                   Fernet
    ${encrypted}=                   Encrypt File and Save       ${SAMPLE_PLAIN_TEXT}
    ...                                                         ${TEMPDIR}/sample.enc
    ${decrypted}=                   Decrypt From File           ${TEMPDIR}/sample.enc
    ${plain_text}=                  Get File                    ${SAMPLE_PLAIN_TEXT}
    Should be Equal as Strings      ${decrypted}                ${plain_text}
    Should not be Equal as Strings  ${encrypted}                ${decrypted}

Test Assymetric
    Switch Engine                   RSA
    ${plain_text}=                  Get File                    ${SMALL_SAMPLE_PLAIN_TEXT}
    ${encrypted}=                   Encrypt                     ${plain_text}
    Should not be Equal as Strings  ${encrypted}                ${plain_text}
    ${decrypted}=                   Decrypt                     ${encrypted}
    Should be Equal as Strings      ${decrypted}                ${plain_text}
    Should not be Equal as Strings  ${encrypted}                ${decrypted}

Test Asymmetric file keywords
    Switch Engine                   RSA
    ${encrypted}=                   Encrypt File and Save       ${SMALL_SAMPLE_PLAIN_TEXT}
    ...                                                         ${TEMPDIR}/sample.enc
    ${decrypted}=                   Decrypt From File           ${TEMPDIR}/sample.enc
    ${plain_text}=                  Get File                    ${SMALL_SAMPLE_PLAIN_TEXT}
    Should be Equal as Strings      ${decrypted}                ${plain_text}
    Should not be Equal as Strings  ${encrypted}                ${decrypted}

Test Larger file encryption using Symmetric with Asymmetric
    [Documentation]                 This is how I suggest you encrypt large files given the limitations of RSA.
    ...                             In general, a file is encrypted using a symmetric-key algorithm, which is then
    ...                             encrypted via RSA encryption. This ensures that only entities with access to the
    ...                             RSA private key will be able to decrypt the symmetric key and retrieve the message.
    Switch Engine                   Fernet
    Encrypt File and Save           ${SAMPLE_PLAIN_TEXT}        ${TEMPDIR}/sample.enc
    Switch Engine                   RSA
    Encrypt File and Save           ${FERNET_KEY}               ${TEMPDIR}/fernet_key.enc
    Decrypt File and Save           ${TEMPDIR}/fernet_key.enc   ${TEMPDIR}/fernet_key.key
    Add Symmetric Engine            Fernet2                     ${TEMPDIR}/fernet_key.key
    Comment                         Setting up a new engine to ensure encrypt/decrypt via RSA was successful
    ${decrypted}=                   Decrypt From File           ${TEMPDIR}/sample.enc
