<%namespace name="base" file="../base.mak"/>
<%inherit file="../base.mak"/>
<form id="synergy-form" class="well form-center" action="#" method="POST">
  <fieldset>
    <legend>
      ${"Synergy"}
      <div class="pull-right">
        <a id="help-button" href="/help/site#synergy" class="btn btn-primary btn-default">Help</a>
      </div>
    </legend>
    <div class="control-group">
      <label class="control-label" for="synergy-title">Title</label>
      <div class="controls">
        <input class="text input-xlarge" id="synergy-title" name="synergy-title" placeholder="(optional)" value="${form_title |n}" />
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="synergy-description">Description</label>
      <div class="controls">
        <textarea class="input-xlarge" id="synergy-description" name="synergy-description" placeholder="(optional)" rows="6">${form_description |n}</textarea>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="synergy-cards">Cards</label>
      <div class="controls">
        <textarea class="input-xlarge" id="synergy-cards" name="synergy-cards" placeholder="9001 Forest" rows="6">${form_cards_text |n}</textarea>
      </div>
    </div>
    <div class="form-actions">
      <button type="submit" class="btn btn-primary btn-large">Synergize!</button>
    </div>
  </fieldset>
</form>
<%block name="js">${base.js_script("/js/jquery.autosize-min.js")}${parent.js()}</%block>
<%block name="js_onready">
$('textarea').autosize();
</%block>
