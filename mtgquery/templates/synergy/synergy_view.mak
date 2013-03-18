<%! import mtgquery.templates.util.common_js as common_js %>
<%! import mtgquery.templates.util as util %>
<%namespace name="components" file="../components.mak"/>
<%namespace name="base" file="../base.mak"/>
<%inherit file="../base.mak"/>
% if view_mode == "regular":
<div class="row-fluid">
  <div class="span8 offset2">
    <div id="notification-area"></div>
  </div>
  <div class="span2"/>
</div>
<div class="well well-small container">
    ${render(title, description, counts, urls, link_alt_href, 'Wide View', new_link_href=copy_from_href)}
</div>
% else:
<div class="row-fluid">
  <div class="span10 offset1">
    ${render(title, description, counts, urls, link_alt_href, 'Regular View', new_link_href=copy_from_href)}
  </div>
  <div class="span1"/>
</div>
% endif
<%def name="render(title, description, counts, urls, link_alt_href=None, link_alt_label='Alt. View', new_link_href='#')">
<h3>
  % if len(title) > 0:
  ${title}
  % else:
  <i>Untitled</i>
  % endif
  % if link_alt_href:
  <a id="synergy-alt-link" href="${link_alt_href}" class="btn btn-primary btn-default pull-right">${link_alt_label}</a>
  % endif
  % if new_link_href is not None:
  <a id="synergy-new-link" href="${new_link_href}" class="btn btn-primary btn-default pull-right">Copy To New</a>
  % endif
</h3>
% if len(description) > 0:
<hr/>
<div class="user-description">
  ${util.mtg_description_escape(description) |n}
</div>
% endif
%if len(urls) > 0:
<hr/>
% for i, (count, url) in enumerate(zip(counts, urls)):
  % if count > 1:
    <% count = '{} Copies'.format(count) %>
  % else:
    <% count = None %>
  % endif
  % if hasattr(url, '__iter__'):
    <% text, url = url %>
  % else:
    <% text = None %>
  % endif
  ${components.captioned_image('synergy-{}'.format(i), 'card-corners', url, text, top_caption=text, bottom_caption=count)}
% endfor
% endif
</%def>

<%block name="js">
${parent.js()}
% if len(notifications) > 0:
${base.js_script("/js/jquery.notifier.js")}
% endif
</%block>

<%block name="js_onready">
% if len(notifications) > 0:
${common_js.notifier_init("notify", "notification-area", 3, notifications=(n.msg for n in notifications)) |n }
% endif
${util.common_js.card_tooltips() |n}
</%block>
