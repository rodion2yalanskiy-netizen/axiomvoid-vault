// Obsidian community plugin — sync auto setup
const obsidian = require('obsidian');

class SyncSetupPlugin extends obsidian.Plugin {
    async onload() {
        console.log('[SyncSetup] Loaded for Бизнес QSNera');
        // Ждём пока sync plugin инициализируется
        this.app.workspace.onLayoutReady(async () => {
            try {
                await this.doSetup();
            } catch(e) {
                console.error('[SyncSetup] Error:', e);
            }
        });
    }
    
    async doSetup() {
        const syncPlugin = this.app.internalPlugins?.plugins?.sync?.instance;
        if (!syncPlugin) {
            console.warn('[SyncSetup] No sync plugin found');
            return;
        }
        if (syncPlugin.vaultId) {
            console.log('[SyncSetup] Already connected to:', syncPlugin.vaultId);
            return;
        }
        console.log('[SyncSetup] Calling setup...');
        await syncPlugin.setup(
            '5495a8fbf4718f27f519d958278c5e32',
            'biznes-qsnera',
            '',
            'ffb9ceb496dcbbffb2193d1fd9f3f188',
            'sync-58.obsidian.md',
            3
        );
        console.log('[SyncSetup] Setup complete!');
    }
    
    onunload() {}
}

module.exports = SyncSetupPlugin;
