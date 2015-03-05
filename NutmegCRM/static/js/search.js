/**
 * Created by justasic on 3/4/15.
 */



var Search = {};

Search.editTimeout = 250.0;

Search.iconSize = 16;

Search.sectionInfo = {
    'invoices':   { heading: 'Invoices:', priority: 3 },
    'customers':  { heading: 'Customers:', priority: 2 },
    'items':      { heading: 'Items:', priority: 1 }
};

/*
 * We could use HTML5's "placeholder" attribute but I don't
 * like how brosers seem to handle it so I will keep it in JS
 */
Search.ToggleDefaultText = function(enable)
{
    this.field.css("display", "inline");

    // Add or remove the class depending on the state.
    this.field.toggleClass("default-text", enable);

    this.hasDefaultText = enable;
    this.field.value = enable ? this.defaultText : "";
};

Search.toggleResults = function(enable)
{
    var res = this.results;
    if (!res)
    {
        if (!enable)
        {
            return;
        }

        res = $('<div>', { id: self.fieldId + "-results",
                           class: "module overlay",
                           style: "width: 25rem; visible: true; zIndex: 10; position: absolute;"
                         });

        this.results = res;

        /*res.setBody("");*/
        /* Append to page body */
        $("body").append(res);
    }

    if (enable)
    {
        /* Recalculate the alignment, in case our context element moved */
        res.align('tl', 'bl');

	    res.show();
    }
    else
    {
	    res.hide();
    }
};

Search.SetCurrentSelection = function(selection)
{
    if (this.selectionList && this.selectionList.length)
    {
        if (selection < 0)
        {
            selection = 0;
        }

        if (selection >= this.selectionList.length)
        {
            selection = this.selectionList.length - 1;
        }

        if (this.currentSelection != null)
        {
            /* TODO */
            this.field.toggleClass('search-selected', false);
            /*YAHOO.util.Dom.removeClass(this.selectionList[this.currentSelection], 'search-selected');*/
        }

        /* YAHOO.util.Dom.addClass(this.selectionList[selection], 'search-selected'); */
        this.field.toggleClass('search-selected', true);
        this.currentSelection = selection;
    }
};

Search.UpdateQuery = function()
{
    var query = this.field.value;

    if (this.field.is(":focus") && query)
    {
        this.ToggleResults(true);

        if (query != this.resultsQuery)
        {
            this.cancel();

            this.resultsQuery = null;
            /* TODO: use $("#w/e").text(query).html() */
            this.results.setBody("Searching for <strong>" + htmlEscape(query) + "</strong>...");

            var self = this;
            this.timer = setTimeout(function() {
                /*
                 * The user stopped editing for a while. Send a search query.
                 */
                self.timer = null;
                self.SendQuery();
            }, this.EditTimeout);
        }
    }
    else
    {
	    this.ToggleResults(false);
    }
};

Search.SendQuery = function()
{
    var self = this;
    var query = this.field.value;

    var ResponseSuccess = function(data)
    {
        self.request = null;
        self.resultsQuery = query;
        try
        {
            self.DisplayResults(obj.results, query);
        }
        catch (e)
        {
            self.results.setBody("Internal error (" + e + ")");
        }
    };

    var ResponseFailure = function(textStatus, errorThrown)
    {
        self.request = null;
        self.resultsQuery = null;
        self.results.setBody("Connection error during search (" + errorThrown + ")");
    };

    /*
     * Must use encodeURIComponent() instead of escape().  escape()
     * will try to encode text in latin-1 (or some other unspecified
     * character set?) and it will emit %u1234-style escapes for other
     * Unicode characters.  encodeURIComponent() generates UTF-8
     * url-encoded text, which is exactly what we want.
     */
    var q = encodeURIComponent(query);

    self.request = $.getJSON(self.url + q, ResponseSuccess);
    self.request.fail(ResponseFailure);
};

Search.cancel = function()
{
    this.selectionList = null;
    this.currentSelection = null;
    this.confirmedQuery = null;

    /*
     * Cancel an existing update timer or connection
     */
    if (this.timer) {
        clearTimeout(this.timer);
        this.timer = null;
    }

    if (this.request)
    {
        this.request.abort();
        this.request = null;
    }
}

Search.DelayedUpdateQuery = function()
{
    /* The new value won't be valid until the event finishes propagating */
    var self = this;
    setTimeout(function() { self.UpdateQuery() }, 0);
};

Search.visitSelection = function(item)
{
    window.location.href = item.href;
};

Search.ToggleResults = function(enable)
{

};

Search.onFocus = function()
{
    if (this.hasDefaultText)
    {
	    this.ToggleDefaultText(false);
    }

    this.UpdateQuery();
};

Search.onBlur = function()
{
    this.UpdateQuery();

    if (this.field.value == "")
    {
        this.ToggleDefaultText(true);
    }
};

Search.onChange = function()
{
    /*
     * This doesn't actually help us in the real world,
     * since browsers only send us onChange when the field
     * is about to blur...
     *
     * Our usual change notifications come via onKeyPress.
     */
    this.DelayedUpdateQuery();
};

Search.onKeypress = function(event)
{
    switch (event.which)
    {
        case 0x26: // up
            if (this.currentSelection != null)
            {
                this.setCurrentSelection(this.currentSelection - 1);
            }

            event.preventDefault();
            break;
        case 0x28: // down
            /*
             * The down arrow can be used, like Enter, to expedite a query-
             * but without the side effect of confirming that query.
             */
            if (this.field.value != this.resultsQuery && !this.request)
            {
                this.cancel();
                this.sendQuery();
            }

            if (this.currentSelection != null)
            {
                this.setCurrentSelection(this.currentSelection + 1);
            }

            event.preventDefault();
            break;
        case 0x0d: // enter
            if (this.field.value)
            {
                if (this.field.value == this.resultsQuery)
                {
                    /* The current query is valid. */

                    if (this.selectionList && this.currentSelection < this.selectionList.length)
                    {
                        /* We have a selection. Make it so! */
                        this.visitSelection(this.selectionList[this.currentSelection]);
                    }
                }
                else
                {
                    if (!this.request)
                    {
                        /* If we don't already have a request in progress, expedite the process */
                        this.cancel();
                        this.sendQuery();
                    }

                    /*
                     * Remember that the user confirmed this query. If we get an exact match later,
                     * visit it immediately. This enables a convenient one-keypress "I'm feeling lucky"
                     * style search.
                     */
                    this.confirmedQuery = this.field.value;
                }
                event.preventDefault();
                break;
            }

        case 0x09: // tab
            break;

        default:
            this.delayedUpdateQuery();
    }
};

Search.init = function(url, fieldId, defaultText)
{
    this.url = url + "?q=";
    this.fieldId = fieldId;
    /* JQuery */
    this.field = $("#search");
    this.field.attr("autocomplete", "off");

    this.defaultText = defaultText;
    this.ToggleDefaultText(true);

    /* Register our JQuery events */
    this.field.focus(this.onFocus);
    this.field.blur(this.onBlur);
    this.field.change(this.onChange);
    this.field.keypress(this.onKeypress);
};