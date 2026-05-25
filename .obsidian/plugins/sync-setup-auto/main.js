// sync-setup-auto v3 — Бизнес QSNera (full debug)
const obsidian = require('obsidian');
const fs = require('fs');

const VAULT_ID   = '5495a8fbf4718f27f519d958278c5e32';
const VAULT_NAME = 'biznes-qsnera';
const HOST       = 'sync-58.obsidian.md';
const LOG        = '/tmp/obsidian-sync-debug.log';

function log(msg) {
    const line = new Date().toISOString() + ' [biznes] ' + msg + '\n';
    try { fs.appendFileSync(LOG, line); } catch(e) {}
    console.log('[SyncSetup]', msg);
}

class SyncSetupPlugin extends obsidian.Plugin {
    async onload() {
        log('Plugin loaded');
        this.app.workspace.onLayoutReady(() => this.doSetup());
    }

    async doSetup() {
        try {
            const sync = this.app.internalPlugins?.plugins?.sync?.instance;
            if (!sync) { log('ERROR: No sync plugin found'); return; }

            log('State: userId=' + sync.userId + ' vaultId=' + (sync.vaultId||'null'));

            if (sync.userId && sync.userId > 0) {
                log('Already connected! userId=' + sync.userId);
                return;
            }

            // Логируем доступные методы
            const proto = Object.getPrototypeOf(sync);
            const methods = Object.getOwnPropertyNames(proto).filter(m => typeof sync[m] === 'function');
            log('Methods: ' + methods.slice(0, 20).join(', '));

            // Пробуем getSharedVaults
            if (typeof sync.getSharedVaults === 'function') {
                try {
                    const vaults = await sync.getSharedVaults();
                    log('Remote vaults: ' + JSON.stringify(vaults));
                } catch(ev) { log('getSharedVaults error: ' + ev.message); }
            }

            log('Calling setup...');
            await sync.setup(VAULT_ID, VAULT_NAME, '', '', HOST, 3);
            log('Setup complete! userId=' + sync.userId);

        } catch (e) {
            log('Setup failed: ' + (e.message || String(e)));
        }
    }

    onunload() {}
}

module.exports = SyncSetupPlugin;
