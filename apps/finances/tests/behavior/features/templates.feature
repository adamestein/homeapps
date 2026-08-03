Feature: Templates

    Scenario: Create Account Template
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Create Template"
        Then the page is verified to be correct

        When the user chooses template type "Account"
        Then the page is verified to be correct

        When the user sets the "Name" to "Account #001"
        And the user sets the "Account number" to "001"
        And the user clicks "Create"
        Then the page is verified to be correct

    Scenario: Create Bill Template
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Create Template"
        Then the page is verified to be correct

        When the user chooses template type "Bill"
        Then the page is verified to be correct

        When the user sets the "Name" to "Bill #1"
        And the user sets the "Account number" to "10101"
        And the user sets the "Amount" to "123.45"
        And the user sets the "Due day" to "12"
        And the user sets the "URL" to "http://pay.bill.com/"
        And the user selects option "option 1 - sample bill option 1"
        And the user selects option "option 2 - sample bill option 2"
        And the user sets the "Snap section" to "1"
        And the user clicks "Create"
        Then the page is verified to be correct

    Scenario: Create Income Template
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Create Template"
        Then the page is verified to be correct

        When the user chooses template type "Income"
        Then the page is verified to be correct

        When the user sets the "Name" to "Paycheck!"
        And the user sets the "Amount" to "5432.17"
        And the user sets the "Arrival day" to "25"
        And the user selects option "option 2 - sample income option 2"
        And the user sets the "Snap section" to "2"
        And the user clicks "Create"
        Then the page is verified to be correct

    Scenario: Edit Account Template (edit values)
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Edit Template"
        Then the page is verified to be correct

        When the user selects Account template "Existing Account #1"
        Then the page is verified to be correct

        When the user sets the "Name" to "New Name"
        And the user sets the "Account Number" to "new acct number"
        And the user clicks "Update"
        Then the page is verified to be correct

    Scenario: Edit Account Template (disable)
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Edit Template"
        Then the page is verified to be correct

        When the user selects Account template "Delete This Account Template"
        Then the page is verified to be correct

        When the user checks "Disabled"
        And the user clicks "Update"
        Then the page is verified to be correct

    Scenario: Edit Bill Template (edit values)
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Edit Template"
        Then the page is verified to be correct

        When the user selects Bill template "Existing Bill #1 for $435.33 due on the 10th of the month"
        Then the page is verified to be correct

        When the user sets the "Name" to "New Name"
        And the user sets the "Account Number" to "new acct number"
        And the user sets the "Amount" to "123.45"
        And the user sets the "Due day" to "25"
        And the user sets the "Url" to "http://pay.me.com/"
        And the user selects option "option 1 - sample bill option 1"
        And the user selects option "option 2 - sample bill option 2"
        And the user sets the "Snap section" to "2"
        And the user clicks "Update"
        Then the page is verified to be correct

    Scenario: Edit Bill Template (disable)
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Edit Template"
        Then the page is verified to be correct

        When the user selects Bill template "Delete This Bill Template due on the 1st of the month"
        Then the page is verified to be correct

        When the user checks "Disabled"
        And the user clicks "Update"
        Then the page is verified to be correct

    Scenario: Edit Income Template (edit values)
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Edit Template"
        Then the page is verified to be correct

        When the user selects Income template "Existing Income #1"
        Then the page is verified to be correct

        When the user sets the "Name" to "Paycheck!"
        And the user sets the "Amount" to "5432.17"
        And the user sets the "Arrival day" to "25"
        And the user selects option "option 2 - sample income option 2"
        And the user sets the "Snap section" to "2"
        And the user clicks "Update"
        Then the page is verified to be correct

    Scenario: Edit Income Template (disable)
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Edit Template"
        Then the page is verified to be correct

        When the user selects Income template "Delete This Income Template"
        Then the page is verified to be correct

        When the user checks "Disabled"
        And the user clicks "Update"
        Then the page is verified to be correct

    Scenario: List Templates
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "List Templates"
        Then the page is verified to be correct
