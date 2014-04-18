#!/usr/bin/env python
import webapp2
from webapp2_extras.routes import RedirectRoute

import tba_config

from controllers.account_controller import AccountEdit, AccountLogout, AccountOverview, AccountRegister
from controllers.ajax_controller import LiveEventHandler, TypeaheadHandler, WebcastHandler
from controllers.event_controller import EventList, EventDetail, EventRss
from controllers.gameday2_controller import Gameday2Controller
from controllers.insights_controller import InsightsOverview, InsightsDetail
from controllers.main_controller import ContactHandler, HashtagsHandler, \
      MainKickoffHandler, MainBuildseasonHandler, MainChampsHandler, MainCompetitionseasonHandler, \
      MainInsightsHandler, MainOffseasonHandler, OprHandler, SearchHandler, \
      AboutHandler, ThanksHandler, PageNotFoundHandler, \
      GamedayHandler, WebcastsHandler, RecordHandler, ApiDocumentationHandler
from controllers.match_controller import MatchDetail
from controllers.suggestions.suggest_match_video_controller import SuggestMatchVideoController
from controllers.suggestions.suggest_event_webcast_controller import SuggestEventWebcastController
from controllers.suggestions.suggest_team_media_controller import SuggestTeamMediaController
from controllers.team_controller import TeamList, TeamCanonical, TeamDetail, TeamHistory

from google.appengine.ext.webapp import template
template.register_template_library('common.my_filters')

landing_handler = {tba_config.KICKOFF: MainKickoffHandler,
                   tba_config.BUILDSEASON: MainBuildseasonHandler,
                   tba_config.CHAMPS: MainChampsHandler,
                   tba_config.COMPETITIONSEASON: MainCompetitionseasonHandler,
                   tba_config.OFFSEASON: MainOffseasonHandler,
                   tba_config.INSIGHTS: MainInsightsHandler,
                   }


class Webapp2HandlerAdapter(webapp2.BaseHandlerAdapter):
    def __call__(self, request, response, exception):
        request.route_args = {}
        request.route_args['exception'] = exception
        handler = self.handler(request, response)
        return handler.get()

app = webapp2.WSGIApplication([
      RedirectRoute(r'/', landing_handler[tba_config.CONFIG['landing_handler']], 'landing', strict_slash=True),
      RedirectRoute(r'/about', AboutHandler, 'about', strict_slash=True),
      RedirectRoute(r'/account', AccountOverview, 'account-overview', strict_slash=True),
      RedirectRoute(r'/account/edit', AccountEdit, 'account-edit', strict_slash=True),
      RedirectRoute(r'/account/register', AccountRegister, 'account-register', strict_slash=True),
      RedirectRoute(r'/apidocs', ApiDocumentationHandler, 'api-documentation', strict_slash=True),
      RedirectRoute(r'/contact', ContactHandler, 'contact', strict_slash=True),
      RedirectRoute(r'/event/<event_key>', EventDetail, 'event-detail', strict_slash=True),
      RedirectRoute(r'/event/<event_key>/feed', EventRss, 'event-rss', strict_slash=True),
      webapp2.Route(r'/events', EventList, 'event-list'),
      webapp2.Route(r'/events/', EventList, 'event-list'),
      RedirectRoute(r'/events/<year:[0-9]+>', EventList, 'event-list', strict_slash=True),
      RedirectRoute(r'/gameday', GamedayHandler, 'gameday', strict_slash=True),
      RedirectRoute(r'/gameday2', Gameday2Controller, 'gameday2', strict_slash=True),
      RedirectRoute(r'/hashtags', HashtagsHandler, 'hashtags', strict_slash=True),
      webapp2.Route(r'/insights', InsightsOverview, 'insights'),
      webapp2.Route(r'/insights/', InsightsOverview, 'insights'),
      webapp2.Route(r'/insights/<year:[0-9]+>', InsightsDetail, 'insights-detail'),
      RedirectRoute(r'/logout', AccountLogout, 'account-logout', strict_slash=True),
      RedirectRoute(r'/match/<match_key>', MatchDetail, 'match-detail', strict_slash=True),
      RedirectRoute(r'/opr', OprHandler, 'opr', strict_slash=True),
      RedirectRoute(r'/record', RecordHandler, 'record', strict_slash=True),
      RedirectRoute(r'/search', SearchHandler, 'search', strict_slash=True),
      RedirectRoute(r'/suggest/event/webcast', SuggestEventWebcastController, 'suggest-event-webcast', strict_slash=True),
      RedirectRoute(r'/suggest/match/video', SuggestMatchVideoController, 'suggest-match-video', strict_slash=True),
      RedirectRoute(r'/suggest/team/media', SuggestTeamMediaController, 'suggest-team-media', strict_slash=True),
      RedirectRoute(r'/team/<team_number:[0-9]+>', TeamCanonical, 'team-canonical', strict_slash=True),
      RedirectRoute(r'/team/<team_number:[0-9]+>/<year:[0-9]+>', TeamDetail, 'team-detail', strict_slash=True),
      RedirectRoute(r'/team/<team_number:[0-9]+>/history', TeamHistory, 'team-history', strict_slash=True),
      webapp2.Route(r'/teams', TeamList, 'team-list'),
      webapp2.Route(r'/teams/', TeamList, 'team-list'),
      webapp2.Route(r'/teams/<page:[0-9]+>', TeamList, 'team-list'),
      RedirectRoute(r'/thanks', ThanksHandler, 'thanks', strict_slash=True),
      RedirectRoute(r'/webcasts', WebcastsHandler, 'webcasts', strict_slash=True),
      webapp2.Route(r'/_/live-event/<event_key>/<timestamp:[0-9]+>', LiveEventHandler, 'ajax-live-event'),
      webapp2.Route(r'/_/typeahead/<search_key>', TypeaheadHandler, 'ajax-typeahead'),
      webapp2.Route(r'/_/webcast/<event_key>/<webcast_number>', WebcastHandler, 'ajax-webcast'),
      webapp2.Route(r'/<:.*>', PageNotFoundHandler, 'page-not-found'),
      ],
      debug=tba_config.DEBUG)
app.error_handlers[404] = Webapp2HandlerAdapter(PageNotFoundHandler)
