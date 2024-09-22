class MicronParser {

    /**
     * Set a custom scheme for urls set on html links.
     * This just makes the browser show a pretty url when hovering links, but in the future, I may implement url
     * interception, rather than using an onclick script on the link element itself.
     */
    static formatNomadnetworkUrl(url) {
        return `nomadnetwork://${url}`;
    }

    /**
     * Converts micron markup to html.
     * FIXME: make sure you can't inject javascript into Reticulum MeshChat browser from micron page content!
     *
     * Known URL Examples:
     * - :
     * - :/page/index.mu
     * - :/page/somefolder/somefile.mu
     * - :/file/somefile.ext
     * - 00000000000000000000000000000000
     * - 00000000000000000000000000000000:/page/index.mu
     * - 00000000000000000000000000000000:/page/somefolder/somefile.mu
     * - 00000000000000000000000000000000:/file/somefile.ext
     * - lxmf@00000000000000000000000000000000
     *
     * References:
     * - https://github.com/markqvist/NomadNet/blob/6a4f2026249b22a00f6ff98c12d06fd5b160a90d/nomadnet/ui/textui/MicronParser.py
     */
    static convertMicronToHtml(markup) {

        console.log(markup);

        // split by line
        var lines = markup.split("\n");

        // parse each line
        lines = lines.map((line) => {

            // skip comments
            if(line.startsWith("#")){
                return null;
            }

            // skip section heading reset
            // FIXME: implement
            if(line === "<"){
                return null;
            }

            // skip background colours
            // FIXME: implement
            line = line.replaceAll(/`B([0-9A-Fa-f]+)/g, function(match, colourCode) {
                return "";
            });

            // skip default background colour
            // FIXME: implement
            line = line.replaceAll(/`b/g, function(match) {
                return "";
            });

            // skip literal
            // FIXME: implement
            line = line.replaceAll(/`=/g, function(match) {
                return "";
            });

            // skip reset formatting
            // FIXME: implement
            if(line.startsWith("``")){
                line = line.replace("``", "");
            }

            // parse micron links
            // `[ ◈  The Future of RNode: A New Model`:/page/posts/2022_06_27.mu]
            // `[Home`:/page/index.mu`page=Home]
            // `[Games`:/page/index.mu`page=Games]
            // `[Hangman`:/page/Games/Hangman.mu]`
            // `[lxmf@7b746057a7294469799cd8d7d429676a]
            // `[Liam`lxmf@7b746057a7294469799cd8d7d429676a]
            line = line.replaceAll(/`\[(.*?)\]/g, function(match, linkContent) {
                const linkParts = linkContent.split("`");
                if(linkParts.length === 1){
                    const url = linkParts[0];
                    const formattedUrl = MicronParser.formatNomadnetworkUrl(url);
                    return `<a href="${formattedUrl}" onclick="event.preventDefault(); onNodePageUrlClick('${url}')">${url}</a>`
                } else if(linkParts.length === 2){
                    const text = linkParts[0];
                    const url = linkParts[1];
                    const formattedUrl = MicronParser.formatNomadnetworkUrl(url);
                    return `<a href="${formattedUrl}" onclick="event.preventDefault(); onNodePageUrlClick('${url}')">${text}</a>`
                } else if(linkParts.length === 3){
                    const text = linkParts[0];
                    const url = linkParts[1] + "`" + linkParts[2]; // includes data
                    const formattedUrl = MicronParser.formatNomadnetworkUrl(url);
                    return `<a href="${formattedUrl}" onclick="event.preventDefault(); onNodePageUrlClick('${url}')">${text}</a>`
                } else {
                    return "";
                }
            });

            // parse markdown links
            // [Reticulum](https://github.com/markqvist/Reticulum)
            line = line.replaceAll(/\[(.*?)\]\((.*?)\)/g, function(match, linkText, linkUrl) {
                const url = MicronParser.formatNomadnetworkUrl(linkUrl);
                return `<a href="${url}" onclick="event.preventDefault(); onNodePageUrlClick('${linkUrl}')" style="text-decoration:underline;">${linkText}</a>`
            });

            // parse bold
            // `!Bold Text
            // `!Bold Text`!
            line = line.replaceAll(/`!(.*?)(?:`!)?/g, function(match, text) {
                return `<span style="font-weight:bold;">${text}</span>`
            });

            // parse italics
            // `*Italic Text`*
            line = line.replaceAll(/`\*(.*?)`\*/g, function(match, text) {
                return `<span style="font-style:italic;">${text}</span>`
            });

            // parse underline
            // `_Underlined Text`_
            line = line.replaceAll(/`_(.*?)`_/g, function(match, text) {
                return `<span style="text-decoration:underline;">${text}</span>`
            });

            // parse divider
            // FIXME: use raw css, not tailwind classes for styling
            if(line.trim() === "-"){
                line = "<hr class='border-gray-500'/>"
            }

            // parse divider (custom character)
            // FIXME: use raw css, not tailwind classes for styling
            // FIXME: use custom divider character
            if(line.startsWith("-") && line.length === 2){
                line = "<hr class='border-gray-500'/>"
            }

            // parse depth (should be full width)
            // FIXME: use raw css, not tailwind classes for styling
            if(line.startsWith(">>>")){
                line = line.replace(">>>", "");
                line = `<span class='inline-block w-full bg-gray-100 text-black pl-3'>${line}</span>`
            } else if(line.startsWith(">>")){
                line = line.replace(">>", "");
                line = `<span class='inline-block w-full bg-gray-100 text-black pl-2'>${line}</span>`
            } else if(line.startsWith(">")){
                line = line.replace(">", "");
                line = `<span class='inline-block w-full bg-gray-100 text-black pl-1'>${line}</span>`
            }

            // align (default: using left)
            if(line.startsWith("`a")){
                line = line.replace("`a", "");
                line = `<span style="text-align:left;">${line}</span>`;
            }

            // align center
            if(line.startsWith("`c")){
                line = line.replace("`c", "");
                line = `<span style="text-align:center;">${line}</span>`;
            }

            // align left
            if(line.startsWith("`l")){
                line = line.replace("`l", "");
                line = `<span style="text-align:left;">${line}</span>`;
            }

            // align right
            if(line.startsWith("`r")){
                line = line.replace("`r", "");
                line = `<span style="text-align:right;">${line}</span>`;
            }

            // formatted content
            // `Ff00 red content `f
            line = line.replaceAll(/`F([0-9A-Fa-f]+)(.*?)`f/g, function(match, colourCode, content) {
                return `<span style="color:#${colourCode}">${content}</span>`
            });

            return line;

        });

        // filter out null items, and join with line break
        return lines.filter((line) => {
            return line != null;
        }).join("<br/>");

    }

}