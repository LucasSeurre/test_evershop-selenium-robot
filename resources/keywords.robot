*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${LOGIN_URL}    http://localhost:3000/admin/login
${EMAIL}        test@test.fr
${PASSWORD}     Blink182

*** Keywords ***
Login Admin
    Go To    ${LOGIN_URL}
    Wait Until Element Is Visible    name=email    10s
    Input Text    name=email    ${EMAIL}
    Input Text    name=password    ${PASSWORD}
    Wait Until Element Is Visible    css=button.button.primary    10s
    Click Button    css=button.button.primary
    Wait Until Page Contains    Dashboard    10s
