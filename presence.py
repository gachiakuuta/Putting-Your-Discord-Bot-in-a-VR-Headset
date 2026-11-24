import discord
import discord.gateway

# Les properties envoyées dans l'IDENTIFY : c'est ce trio qui
# fait ranger la session dans le slot "vr" côté Discord.
PROPERTIES_VR = {
    "os": "android",
    "browser": "Discord VR",
    "device": "Discord VR",
}


def installer_patch_identify():
    """Remplace identify() pour injecter nos properties.

    Copie conforme de l'originale de discord.py 2.7.1 : si tu es
    sur une autre version, recopie le corps de TA version et ne
    change que le bloc properties. À appeler avant bot.run().
    """

    async def identify(self):
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "properties": PROPERTIES_VR,   # <-- la seule ligne qui change
                "compress": True,
                "large_threshold": 250,
            },
        }

        if self.shard_id is not None and self.shard_count is not None:
            payload["d"]["shard"] = [self.shard_id, self.shard_count]

        state = self._connection
        if state._activity is not None or state._status is not None:
            payload["d"]["presence"] = {
                "status": state._status,
                "game": state._activity,
                "since": 0,
                "afk": False,
            }

        if state._intents is not None:
            payload["d"]["intents"] = state._intents.value

        await self.call_hooks("before_identify", self.shard_id,
                              initial=self._initial_identify)
        await self.send_as_json(payload)

    discord.gateway.DiscordWebSocket.identify = identify
