<%! 
  import mtgquery.templates.util.common_js as common_js
%>
<%namespace name="base" file="../components/base.mak"/>
<%namespace name="components" file="../components/components.mak"/>
<%def name="render(name, data_1, data_2, gt_1, gt_2, diff, headers, link_alt_href=None, link_alt_label='Alt. View')">

<div class="row-fluid">
  <div class="span12 well well-small">
    <h3>
      % if len(name) > 0:
      ${name}
      % endif
      % if link_alt_href:
      <a id="trade-alt-link" href="${link_alt_href}" class="btn btn-primary btn-default pull-right">${link_alt_label}</a>
      % endif
    </h3>
    % if len(name) > 0:
    <hr/>
    % endif
    <div class="trade-summary">
      <div class = "summary-column">
        <div>Stack 1</div>
        <div>$${gt_1}</div>
      </div>
      <div class = "summary-column">
        <div>Stack 2</div>
        <div>$${gt_2}</div>
      </div>
      <div class = "summary-column">
        <div>Diff</div>
        <div>$${diff}</div>
      </div>
    </div>
    <hr/>
    <div class="row-fluid">
      <div class="span12">
        <label class="label label-x-large" for="card_table_1">Stack One</label>
        ${components.basic_table(data_1, headers, "card_table_1")}
      </div>
    </div>
    <div class="row-fluid">
      <div class="span12">
        <label class="label label-x-large" for="card_table_2">Stack Two</label>
        ${components.basic_table(data_2, headers, "card_table_2")}
      </div>
    </div>    
  </div>
</div>


</%def>

<%def name="render_css()">
${base.css_link('/css/theme.bootstrap.css', 'screen')}
</%def>

<%def name="render_js()">
${base.js_script("/js/jquery.tablesorter.min.js")}
${base.js_script("/js/jquery.tablesorter.widgets.min.js")}
</%def>

<%def name="render_js_onready()">
${common_js.tablesort_init("card_table_1") | n}
${common_js.tablesort_init("card_table_2") | n}
${common_js.tablesort_bootstrap_theme() |n}
</%def>