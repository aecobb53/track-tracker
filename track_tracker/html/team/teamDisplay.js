async function teamDisplay(displayType) {
    console.log('Changing Display Type: ' + displayType);
    var expectedClass = 'page-content-' + displayType.toLowerCase();
    var displayItem = document.getElementsByClassName("display-item-activated");
    for ( i = 0; i < displayItem.length; i++) {
        let pageContent = displayItem[i]
        if (pageContent.classList.contains(expectedClass)) {
            pageContent.removeAttribute('hidden');
        } else {
            pageContent.setAttribute('hidden', '');
        }
    }
    var displayItem = document.getElementsByClassName("display-item-deactivated");
    for ( i = 0; i < displayItem.length; i++) {
        let pageContent = displayItem[i]
        if (pageContent.classList.contains(expectedClass)) {
            pageContent.removeAttribute('hidden');
        } else {
            pageContent.setAttribute('hidden', '');
        }
    }

    // Buttons
    var expectedClass = 'button-item-' + displayType.toLowerCase();
    var displayItem = document.getElementsByClassName("team-display-button");
    for ( i = 0; i < displayItem.length; i++) {
        let pageContent = displayItem[i]
        if (pageContent.classList.contains(expectedClass)) {
            pageContent.classList.add('button-activated');
            pageContent.classList.remove("button-deactivated");
        } else {
            pageContent.classList.add('button-deactivated');
            pageContent.classList.remove("button-activated");
        }
    }
}
