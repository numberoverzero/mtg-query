<%inherit file="../base.mak"/>
<div class="well well-small container">
% for synergy in synergies:
  <a href="${synergy['url']}"><div class="well">
    <h3>${synergy['title']}</h3>
    <span>${synergy['length']} cards</span>
  </div></a>
% endfor
</div>
