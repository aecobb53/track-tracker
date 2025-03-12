
async function toggleCheckboxes(checkboxClass) {
    console.log('Toggling Checkboxes');
    let displayCheckboxInput = document.getElementsByClassName(checkboxClass);
    console.log(displayCheckboxInput);
    var all_checked = true;
    var some_checked = false;
    for ( i = 0; i < displayCheckboxInput.length; i++) {
        if (displayCheckboxInput[i].checked) {
            some_checked = true;
        } else {
            all_checked = false;
        }
    }
    if ( all_checked) {
        console.log('All checked');
        for ( i = 0; i < displayCheckboxInput.length; i++) {
            displayCheckboxInput[i].checked = false;
        }
    } else if ( !all_checked && some_checked) {
        console.log('Some checked');
        for ( i = 0; i < displayCheckboxInput.length; i++) {
            displayCheckboxInput[i].checked = true;
        }
    } else {
        console.log('None checked');
        for ( i = 0; i < displayCheckboxInput.length; i++) {
            displayCheckboxInput[i].checked = true;
        }
    }
}

// async function toggleCheckboxesContributions() {
//     console.log('Toggling Checkboxes Contributions');
//     toggleCheckboxes("contributions-checkbox-group");
// }

// async function toggleCheckboxesAdj() {
//     console.log('Toggling Checkboxes Adj');
//     toggleCheckboxes("adj-checkbox-group");
// }

// async function toggleCheckboxesNetWorth() {
//     console.log('Toggling Checkboxes NetWorth');
//     toggleCheckboxes("net-worth-checkbox-group");
// }

// async function toggleCheckboxesTaxes() {
//     console.log('Toggling Checkboxes Taxes');
//     toggleCheckboxes("taxes-checkbox-group");
// }

// async function toggleCheckboxesInterest() {
//     console.log('Toggling Checkboxes Interest');
//     toggleCheckboxes("interest-checkbox-group");
// }

// async function toggleCheckboxesAccounts() {
//     console.log('Toggling Checkboxes Accounts');
//     toggleCheckboxes("accounts-checkbox-group");
// }

// async function toggleCheckboxesIncomeAndExpenses() {
//     console.log('Toggling Checkboxes IncomeAndExpenses');
//     toggleCheckboxes("income-and-expenses-checkbox-group");
// }

async function toggleCheckboxesAll() {
    console.log('Toggling all Checkboxes');
    toggleCheckboxes("display-checkbox-input");
}

// Add houses?
// Add other big loans - Mortgages?
// Change checkboxes to update like the apply button when clicked
// Add more dummy data
// Add a testing button that populates data so i can move the extra blcok out of the main code