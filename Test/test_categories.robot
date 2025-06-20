*** Settings ***
Library           SeleniumLibrary
Resource          ../resources/keywords.robot
Test Setup        Open Browser To Login Page
Test Teardown     Close Browser


*** Variables ***
${LOGIN_URL}              http://localhost:3000/admin/login
${CATEGORY_NAME}          Chaussures
${UPDATED_CATEGORY_NAME}  Chaussures pour femme

*** Test Cases ***
Test Gestion Catégories
    Login Admin
    Aller à la page Categories
    Créer une Nouvelle Catégorie
    Vérifier Succès Création
    Modifier la Catégorie
    Vérifier Succès Modification
    Supprimer la Catégorie
    Vérifier Suppression

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN_URL}    Chrome
    Maximize Browser Window

Aller à la page Categories
    Wait Until Element Is Visible    css=a[href$="/admin/categories"]    10s
    Click Element    css=a[href$="/admin/categories"]
    Wait Until Page Contains    Categories    10s


Créer une Nouvelle Catégorie
    Wait Until Element Is Visible    css=a[href$="/admin/categories/new"]    10s
    Click Element    css=a[href$="/admin/categories/new"]
    Wait Until Element Is Visible    css=input#name    10s
    Clear Element Text    css=input#name
    Input Text    css=input#name    ${CATEGORY_NAME}
    Clear Element Text    css=input#urlKey
    Input Text            css=input#urlKey    Chaussures
    Clear Element Text    css=input#metaTitle
    Input Text            css=input#metaTitle    Chaussures
    Clear Element Text    css=input#metakeywords
    Input Text            css=input#metakeywords    Chaussures
    Clear Element Text    css=textarea#meta_description
    Input Text            css=textarea#meta_description    Chaussures
    Click Element    css=button.button.primary

Vérifier Succès Création
    Wait Until Page Contains Element    css=.Toastify__toast--success    10s
    Page Should Contain    Category saved successfully!

Modifier la Catégorie
    Aller à la page Categories
    Wait Until Element Is Visible    css=a.font-semibold[href*="/admin/categories/edit"]    10s
    Click Element    css=a.font-semibold[href*="/admin/categories/edit"]
    Wait Until Element Is Visible    css=input#name    10s
    Clear Element Text    css=input#name
    Input Text    css=input#name    ${UPDATED_CATEGORY_NAME}
    Click Element    css=button.button.primary

Vérifier Succès Modification
    Wait Until Page Contains Element    css=.Toastify__toast--success    10s
    Page Should Contain    Category saved successfully!

Supprimer la Catégorie
    Aller à la page Categories
    Wait Until Page Contains    ${UPDATED_CATEGORY_NAME}    10s
    Click Element    css=tr:nth-of-type(2) .checkbox-unchecked

    Click Element    xpath=//span[contains(text(),"Delete")]
    Wait Until Page Contains    Delete 1 categories    10s
    Wait Until Element Is Visible    css=button.critical
    Click Element    css=button.critical
    Sleep    2s

Vérifier Suppression
    Aller à la page Categories
    Input Text    css=input#name    ${UPDATED_CATEGORY_NAME}
    Press Keys    css=input#name    RETURN
    Sleep    1s
    ${resultats} =  Get Element Count    css=table.listing tbody tr:has(td)
    Should Be Equal    ${resultats}    ${0}