// sync-setup-auto v2 — Бизнес QSNera
const obsidian = require('obsidian');

const VAULT_ID   = '5495a8fbf4718f27f519d958278c5e32';
const VAULT_NAME = 'biznes-qsnera';
const VAULT_SALT = 'ffb9ceb496dcbbffb2193d1fd9f3f188';
const HOST       = 'sync-58.obsidian.md';

class SyncSetupPlugin extends obsidian.Plugin {
    async onload() {
        console.log('[SyncSetup] Loaded — ' + VAULT_NAME);
        this.app.workspace.onLayoutReady(() => this.doSetup());
    }

    async doSetup() {
        try {
            const syncPlugin = this.app.internalPlugins?.plugins?.sync?.instance;
            if (!syncPlugin) {
                console.warn('[SyncSetup] Sync plugin not found');
                return;
            }
            // userId > 0 = уже авторизован через Obsidian Sync
            if (syncPlugin.userId && syncPlugin.userId > 0) {
                console.log('[SyncSetup] Already connected, userId=' + syncPlugin.userId);
                return;
            }
            console.log('[SyncSetup] Connecting to remote vault...');
            await syncPlugin.setup(VAULT_ID, VAULT_NAME, '', VAULT_SALT, HOST, 3);
            console.log('[SyncSetup] Setup complete! userId=' + syncPlugin.userId);
        } catch (e) {
            console.error('[SyncSetup] Setup failed:', e.message || e);
        }
    }

    onunload() {}
}

module.exports = SyncSetupPlugin;
