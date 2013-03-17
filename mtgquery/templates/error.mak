<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3/org/1999/xhtml">
  <head>
    <style type="text/css">
      html {text-align:center;}
      #line1 {font-size: 22px; line-height:24px;font-weight:bold;}
      #line2 {font-size: 20px; line-height:22px; font-style:italic}
    </style>
  </head>
  <body>
    % if img:
    <img src="${img}" alt="error image" />
    % endif
    % if line1:
    <div id="line1">${line1}</div>
    % endif
    % if line2:
    <div id="line2">${line2}</div>
    % endif
  </body>
</html>