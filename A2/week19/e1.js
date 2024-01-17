function convertPermission() {
    let input = document.getElementById('permissionInput').value;
    let result = permissionToOctal(input);
    document.getElementById('result').innerText = 'Octal: ' + result;
}

function permissionToOctal(permissionString) {
    const permissionMap = { 'r': 4, 'w': 2, 'x': 1, '-': 0 };
    let octal = '';

    for (let i = 0; i < 9; i += 3) {
        let sum = 0;
        for (let j = i; j < i + 3; j++) {
            sum += permissionMap[permissionString[j]];
        }
        octal += sum.toString();
    }

    return octal;
}
