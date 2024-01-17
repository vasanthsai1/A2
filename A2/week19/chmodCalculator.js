function calculatePermissions() {
    const permissions = {
        owner: getPermissionSet('owner'),
        group: getPermissionSet('group'),
        others: getPermissionSet('others')
    };

    const symbolic = convertToSymbolic(permissions);
    const octal = convertToOctal(permissions);
    document.getElementById('result').innerText = `Symbolic: ${symbolic}, Octal: ${octal}`;
}

function getPermissionSet(userType) {
    return {
        read: document.getElementById(`${userType}Read`).checked,
        write: document.getElementById(`${userType}Write`).checked,
        execute: document.getElementById(`${userType}Execute`).checked,
    };
}

function convertToSymbolic(permissions) {
    let symbolic = '';
    for (let key of ['owner', 'group', 'others']) {
        symbolic += (permissions[key].read ? 'r' : '-');
        symbolic += (permissions[key].write ? 'w' : '-');
        symbolic += (permissions[key].execute ? 'x' : '-');
    }
    return symbolic;
}

function convertToOctal(permissions) {
    let octal = '';
    for (let key of ['owner', 'group', 'others']) {
        let value = 0;
        value += permissions[key].read ? 4 : 0;
        value += permissions[key].write ? 2 : 0;
        value += permissions[key].execute ? 1 : 0;
        octal += value.toString();
    }
    return octal;
}
