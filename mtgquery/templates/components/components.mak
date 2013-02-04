<%! 
  import mtgquery.templates.util.util as util
  import mtgquery.templates.util.common_js as common_js

  def active(condition):
    return 'active' if condition else ''
%>
<%def name="navbar(brand, brand_link, labels, hrefs, selected_label)">
<div class="container">
  <div class="navbar">
    <div class="navbar-inner">
      <a class="brand" href="${brand_link}">${brand}</a>
      %if len(labels) > 0:
      <ul class="nav pull-right">
        % for index, label, href in util.izip(labels, hrefs):
        <li class="${active(label == selected_label)}"><a href="${href}">${label}</a></li>
        % endfor
      </ul>
      % endif
    </div>
  </div>
</div>
</%def>

<%def name="tabs(labels, contents, selected_index)">
<div class="tabbable">
  <ul class="nav nav-tabs">
    % for index, label in enumerate(labels):
    <li class="${active(index == selected_index)}"><a href="#tab${index}" data-toggle="tab">${label}</a></li>
    % endfor
  </ul>
  <div class="tab-content">
    % for index, label, content in util.izip(labels, contents):
    <div class="tab-pane ${active(index == selected_index)}" id="tab${index}">
      ${content |n}
    </div>
    % endfor
  </div>
</div>
</%def>

<%def name="outline(sections, header, list, list_classes=None)">
<% list_classes = [] if list_classes is None else list_classes %>
% for section in sections:
  <${header}>
    ${section['header']}
    <small>${section['subheader']}</small>
  </${header}>
  % if 'contents' in section and len(section['contents']) > 0:
  <% list_class = " ".join(list_classes) %>
  <${list} class="${list_class}">
  % for list_item in section['contents']:
    <li>${list_item |n}</li>
  % endfor
  </${list}>
  % endif
% endfor
</%def>

<%def name="basic_table(data, headers, table_id)">
<table id="${table_id}" class="table tablesorter">
  <thead>
    <tr>
      % for header in headers:
      <th>${header}</th>
      % endfor
    </tr>
  </thead>
  <tbody>
    % for row in data:
    <tr>
      % for col in row:
      <td>${col}</td>
      %endfor
    </tr>
    % endfor
  </tbody>
</table>
</%def>

<%def name="buttonpopover(content, label, title, placement='right', style='info', size='default', escape_content=False)">
<% content = util.ifelse(escape_content, util.url_escape(content), content) %>
<a href="#" class="btn btn-${size} btn-${style}" rel="popover" title="${title}" data-placement="${placement}" data-content="${content}">${label}</a>
</%def>

<%def name="captioned_image(id, src, alt, top_caption=None, bottom_caption=None)">
<div id="${id}" class="captioned-image">
  <dt><img id="${id}-img" src="${src |n}" alt="${alt or '' |n}" /></dt>
  <dd class="top-caption" id="${id}-caption-top">
  % if top_caption is not None:
  % for line in top_caption.split('\n'):
  <p>${line |n}</p>
  % endfor
  % endif
  </dd>
  <dd class="bottom-caption" id="${id}-caption-bottom">
  % if bottom_caption is not None:
  % for line in bottom_caption.split('\n'):
  <p>${line |n}</p>
  % endfor
  % endif
  </dd>
</div>
</%def>