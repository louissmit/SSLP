def alignment(e, f, a):
    args = {'id': 'svg'+hex(hash(e+f+str(a))), 'e': e, 'f': f, 'a': str(a)}
    return """
    <svg id="%(id)s" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%%" height="50"></svg>
    <script type="text/javascript">
    var e = "%(e)s", f = "%(f)s", a = %(a)s;
    var svgNS = "http://www.w3.org/2000/svg";
    var svg = document.getElementById("%(id)s");
    function svgSet(obj, dictionary) {
        for (var key in dictionary) {
            if (dictionary.hasOwnProperty(key)) {
                obj.setAttributeNS(null,key, dictionary[key]);
            }
        }
        return obj;
    }
    var h = 50;
    var sentence = function(top, words) {
        words = words.split(' ');
        var t = svgSet(document.createElementNS(svgNS,"text"), {
            "x": 0,
            "y": top,
            "text-anchor": "start",
            "style": "font-size:10px; font-family: Arial;"
        });
        svg.appendChild(t);
        var tempText = "", tempWidth = 0, widths = [];
        for (var i=0; i<words.length; i++) {
          t.textContent = tempText += " " + words[i];
          widths.push(tempWidth + (t.getBBox().width-tempWidth)/2);
          tempWidth = t.getBBox().width;
        }
        return widths;
    };
    var t = 10, b = h-10;
    ew = sentence(t, e);
    fw = sentence(b, f);
    a.forEach(function(al) {
        svg.appendChild(
            svgSet(document.createElementNS(svgNS,"path"), {
                "fill": "none",
                "stroke": "#ff0000",
                "d": "M"+ew[al[1]]+","+(t + 5)+"L"+fw[al[0]]+","+(b - 5)+""
            }));
    });
    </script>
    """ % args