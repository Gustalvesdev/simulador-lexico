const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
    testDir: './tests',
    fullyParallel: false,
    reporter: 'list',
    use: {
        baseURL: 'http://127.0.0.1:8080',
        browserName: 'chromium',
        headless: true,
    },
});
