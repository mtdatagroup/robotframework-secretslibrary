*** Settings ***
Library                         SecretsLibrary
Library                         OperatingSystem

*** Variables ***
${TESTDATA_DIRECTORY}           ${CURDIR}${/}..${/}testdata
${SAMPLE_PLAIN_TEXT}            ${TESTDATA_DIRECTORY}${/}sample.txt
${SMALL_SAMPLE_PLAIN_TEXT}      ${TESTDATA_DIRECTORY}${/}small_sample.txt

${FERNET_KEY}                   ${TESTDATA_DIRECTORY}${/}symmetric${/}/symmetric_key.key
${PRIVATE_KEY}                  ${TESTDATA_DIRECTORY}${/}asymmetric${/}/private_key.pem
${PUBLIC_KEY}                   ${TESTDATA_DIRECTORY}${/}asymmetric${/}/public_key.pem

*** Keywords ***
Configure Engines
    [Documentation]             Setting up both Fernet and RSA for testing
    Add Symmetric Engine        Fernet              ${FERNET_KEY}
    Add Asymmetric Engine       RSA                 ${PRIVATE_KEY}
    ...                                             ${PUBLIC_KEY}

Encrypt File and Save
    [Documentation]             This will read a (plain text) file and write results to (encrypted) file
    [Arguments]                 ${in_path}          ${out_path}
    ${encrypted}=               Encrypt File        ${in_path}
    Create Binary File          ${out_path}         ${encrypted}
    [Return]                    ${encrypted}

Decrypt File and Save
    [Documentation]             This will read an ecypted file and write the decrypted results to another file
    [Arguments]                 ${in_path}          ${out_path}
    ${decrypted}=               Decrypt From File   ${in_path}
    Create Binary File          ${out_path}         ${decrypted}
    [Return]                    ${decrypted}