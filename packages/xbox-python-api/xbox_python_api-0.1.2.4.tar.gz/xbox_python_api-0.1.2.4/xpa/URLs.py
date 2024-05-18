class URLs:
    def __init__(self):
        self.base_url = "https://xbl.io/api/v2/"

        # account
        self.account_xuid = "account/{xuid}"
        self.search_gamertag = "search/{gamertag}"
        self.xuid_presence = "{xuid}/presence"

        # achievements
        self.achievements_xuid = "achievements/player/{xuid}"
        self.title_achievements_xuid = "achievements/player/{xuid}/{titleId}"
        self.title360_achievements_xuid = "achievements/player/{xuid}/title/{titleId}"
        self.player360_achievements_xuid = "achievements/x360/{xuid}/title/{titleId}"

        # clubs
        self.club_details = "clubs/{clubId}"

        # friends
        self.friends_xuid = "friends/{xuid}"
        self.search_friend = "friends/search/{gamertag}"

        # gamepass
        self.gamepass_all = "gamepass/all"
        self.gamepass_pc = "gamepass/pc"
        self.gamepass_eaplay = "gamepass/ea-play"
        self.gamepass_nocontroller = "gamepass/no-controller"

        # marketplace
        self.marketplace_new = "marketplace/new"
        self.marketplace_toppaid = "marketplace/top-paid"
        self.marketplace_bestrated = "marketplace/best-rated"
        self.marketplace_comingsoon = "marketplace/coming-soon"
        self.marketplace_deals = "marketplace/deals"
        self.marketplace_topfree = "marketplace/top-free"
        self.marketplace_mostplayed = "marketplace/most-played"
        self.marketplace_searchgame = "marketplace/title/{titleId}"

        # player
        self.player_summary = "player/summary/{xuid}"
        self.player_titleHistory = "player/titleHistory/{xuid}"

        # session
        self.session_details = "session/{sessionName}"

        # group
        self.group_summary = "group/summary/{groupId}"
        self.group_messages = "group/messages/{groupId}"

    def base_url(self):
        return self.base_url

    def account_xuid_url(self, xuid):
        return self.base_url + self.account_xuid.format(xuid=xuid)

    def search_gamertag_url(self, gamertag):
        return self.base_url + self.search_gamertag.format(gamertag=gamertag)

    def xuid_presence_url(self, xuid):
        return self.base_url + self.xuid_presence.format(xuid=xuid)

    def achievements_xuid_url(self, xuid):
        return self.base_url + self.achievements_xuid.format(xuid=xuid)

    def title_achievements_xuid_url(self, xuid, titleId):
        return self.base_url + self.title_achievements_xuid.format(xuid=xuid, titleId=titleId)

    def title360_achievements_xuid_url(self, xuid, titleId):
        return self.base_url + self.title360_achievements_xuid.format(xuid=xuid, titleId=titleId)

    def player360_achievements_xuid_url(self, xuid, titleId):
        return self.base_url + self.player360_achievements_xuid.format(xuid=xuid, titleId=titleId)

    def club_details_url(self, clubId):
        return self.base_url + self.club_details.format(clubId=clubId)

    def friends_xuid_url(self, xuid):
        return self.base_url + self.friends_xuid.format(xuid=xuid)

    def search_friend_url(self, gamertag):
        return self.base_url + self.search_friend.format(gamertag=gamertag)

    def gamepass_all_url(self):
        return self.base_url + self.gamepass_all

    def gamepass_pc_url(self):
        return self.base_url + self.gamepass_pc

    def gamepass_eaplay_url(self):
        return self.base_url + self.gamepass_eaplay

    def gamepass_nocontroller_url(self):
        return self.base_url + self.gamepass_nocontroller

    def marketplace_new_url(self):
        return self.base_url + self.marketplace_new

    def marketplace_toppaid_url(self):
        return self.base_url + self.marketplace_toppaid

    def marketplace_bestrated_url(self):
        return self.base_url + self.marketplace_bestrated

    def marketplace_comingsoon_url(self):
        return self.base_url + self.marketplace_comingsoon

    def marketplace_deals_url(self):
        return self.base_url + self.marketplace_deals

    def marketplace_topfree_url(self):
        return self.base_url + self.marketplace_topfree

    def marketplace_mostplayed_url(self):
        return self.base_url + self.marketplace_mostplayed

    def marketplace_searchgame_url(self, titleId):
        return self.base_url + self.marketplace_searchgame.format(titleId=titleId)

    def player_summary_url(self, xuid):
        return self.base_url + self.player_summary.format(xuid=xuid)

    def player_titleHistory_url(self, xuid):
        return self.base_url + self.player_titleHistory.format(xuid=xuid)

    def session_details_url(self, sessionName):
        return self.base_url + self.session_details.format(sessionName=sessionName)

    def group_summary_url(self, groupId):
        return self.base_url + self.group_summary.format(groupId=groupId)

    def group_messages_url(self, groupId):
        return self.base_url + self.group_messages.format(groupId=groupId)
