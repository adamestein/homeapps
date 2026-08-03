Feature: Tracker

    Scenario: Track Payments
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Track Payments"
        And the user selects statement "December 15th, 2019"
        Then the page is verified to be correct

        When the user selects the "Unfunded" bill "old bill 1 for $34.45 due on December 28th, 2019"
        Then the page is verified to be correct

        When the user selects the "Unpaid" bill "old bill 1 for $34.45 due on December 28th, 2019"
        Then the page is verified to be correct

        When the user sets the "Actual" to "111.22"
        And the user selects Payment method "ACH - Direct Debit"
        And the user sets the "Confirmation number" to "abc123"
        And the user clicks "Ok"
        Then the page is verified to be correct
        And the confirmation number is verified to be correct
