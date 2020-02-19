Feature: Statements

    Scenario: Create Statement
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Create Statement"
        Then the page is verified to be correct

        When the user creates a new "account" item
        Then the page is verified to be correct

        When the user sets the "Name" to "Account #001"
        And the user sets the "Account number" to "001"
        And the user sets the "Amount" to "32.55"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user chooses the existing "account" item "Existing Account #1"
        Then the page is verified to be correct

        When the user sets the "Amount" to "225.99"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user creates a new "bill" item
        Then the page is verified to be correct

        When the user sets the "Name" to "Bill #1"
        And the user sets the "Account number" to "10101"
        And the user sets the "Amount" to "123.45"
        And the user sets the "Total" to "500"
        And the user sets the "Date" to "01/15/2020"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user chooses the existing "bill" item "Existing Bill #1"
        Then the page is verified to be correct

        When the user clicks "Ok"
        Then the page is verified to be correct

        When the user creates a new "income" item
        Then the page is verified to be correct

        When the user sets the "Name" to "Paycheck!"
        And the user sets the "Amount" to "5432.17"
        And the user sets the "Date" to "01/02/2020"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user chooses the existing "income" item "Existing Income #1"
        Then the page is verified to be correct

        When the user sets the "Date" to "01/09/2020"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user clicks "Create"
        Then the page is verified to be correct

        When the user clicks "Create Statement"
        Then the page is verified to be correct

    Scenario: Edit Statement
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Edit Statement"
        Then the page is verified to be correct

        When the user hovers over the year "2019" and selects the statement for "December 15th, 2019"
        Then the page is verified to be correct

        When the user clicks "old account 1 (acct #old acct #1) with US$0.03"
        Then the page is verified to be correct

        When the user sets the "Amount" to "123.45"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user creates a new "account" item
        And the user sets the "Name" to "New Account #001"
        And the user sets the "Account number" to "001"
        And the user sets the "Amount" to "32.55"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user deletes "old account 2 (acct #old acct #2) with US$445.98"
        Then the page is verified to be correct

        When the user deletes "old bill 1 for $34.45 (total is $100.00) due on December 28th, 2019"
        Then the page is verified to be correct

        When the user clicks "old bill 2 for $40.00 due on December 20th, 2019"
        And the user sets the "Total" to "100"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user creates a new "bill" item
        And the user sets the "Name" to "Bill #1"
        And the user sets the "Account number" to "10101"
        And the user sets the "Amount" to "123.45"
        And the user sets the "Total" to "500"
        And the user sets the "Date" to "01/15/2020"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user deletes "old income 1 for $4,539.34 deposited on December 16th, 2019 into account #old income #1"
        And the user deletes "old income 2 for $450.00 deposited on December 17th, 2019"
        Then the page is verified to be correct

        When the user creates a new "income" item
        And the user sets the "Name" to "Paycheck!"
        And the user sets the "Amount" to "5432.17"
        And the user sets the "Date" to "01/02/2020"
        And the user clicks "Ok"
        Then the page is verified to be correct

        When the user clicks "Update"
        Then the page is verified to be correct

        When the user clicks "Update Statement"
        Then the page is verified to be correct

    Scenario: View Previous Statements
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "View Previous Statements"
        Then the page is verified to be correct

        When the user hovers over the year "2019" and selects the statement for "December 15th, 2019"
        Then the page is verified to be correct

        When the user downloads the PDF version of the statement
        Then the PDF file is verified to be correct
