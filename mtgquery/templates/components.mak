<%! 
  def active(condition):
    return 'active' if condition else ''
%>
<%def name="navbar(brand, brand_link, left_links, right_links, selected_label)">
<div class="navbar navbar-inverse">
  <div class="navbar-inner">
    <a class="brand" href="${brand_link}">${brand}</a>
    <div class="nav-collapse">
      <ul class="nav">
        % for label, href in zip(*left_links):
        <li class="${active(label == selected_label)}"><a href="${href}">${label}</a></li>
        % endfor
      </ul>
      <ul class="nav pull-right">
        % for label, href in zip(*right_links):
        <li class="${active(label == selected_label)}"><a href="${href}">${label}</a></li>
        % endfor
      </ul>
    </div>
  </div>
</div>
</%def>

<%def name="captioned_image(id, classt, src, alt, top_caption=None, bottom_caption=None)">
<div id="${id}" class="captioned-image">
  <dt><img id="${id}-img" class="${classt}" src="${src |n}" alt="${alt or '' |n}" /></dt>
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
