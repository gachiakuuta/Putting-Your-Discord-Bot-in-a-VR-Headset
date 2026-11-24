from presence import installer_patch_identify

installer_patch_identify()   # AVANT bot.run(), sinon l'IDENTIFY est déjà parti
bot.run(TOKEN)
