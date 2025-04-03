function signIn(provider) {
    let url = "#";
    switch (provider) {
        case 'Google':
            url = "https://accounts.google.com/signin";
            break;
        case 'Apple':
            url = "https://appleid.apple.com/auth/authorize";
            break;
        case 'GoFloww':
            url = "https://gofloww.com/signin";
            break;
    }
    window.open('url', '_blank')
}