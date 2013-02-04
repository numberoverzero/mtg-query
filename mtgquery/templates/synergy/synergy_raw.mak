<%namespace name="base" file="../components/base.mak"/>
<%namespace name="components" file="../components/components.mak"/>
<%! import mtgquery.templates.util as util %>

<%def name="render(name, description, counts, urls, link_alt_href=None, link_alt_label='Alt. View', new_link_href='#')">
<div class="row-fluid">
  <div class="span12 well well-small">
    <h3>
      % if len(name) > 0:
      ${name}
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
  </div>
</div>
<div class="row-fluid">
  %if len(urls) > 0:
  <div class="span12 well well-small" id="synergy-cards">
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
    ${components.captioned_image('synergy-{}'.format(i), url, text, top_caption=text, bottom_caption=count)}
  % endfor
  </div>
  % endif
</div>
</%def>

<%def name="js_onready()">
${util.common_js.card_tooltips() |n}
</%def>