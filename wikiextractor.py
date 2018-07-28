
#     line = s

#     useLinkPrefixExtension = self.getTargetLanguage().linkPrefixExtension()
#     e2 = None
#     if useLinkPrefixExtension:
#         # Match the end of a line for a word that is not followed by whitespace,
#         # e.g. in the case of "The Arab al[[Razi]]",  "al" will be matched
#         global wgContLang
#         charset = wgContLang.linkPrefixCharset()
#         e2 = re.compile("((?>.*[^charset]|))(.+)", re.S | re.D | re.U)

#     if self.mTitle is None:
#         raise MWException(__METHOD__ + ": \self.mTitle is null\n")

#     nottalk = not self.mTitle.isTalkPage()

#     if useLinkPrefixExtension:
#         m = e2.match(s)
#         if m:
#             first_prefix = m.group(2)
#         else:
#             first_prefix = false
#     else:
#         prefix = ''

#     useSubpages = self.areSubpagesAllowed()

#     for m in iterBrackets:
#         line = text[cur:m.start()]
#         cur = m.end()

#         # TODO: Check for excessive memory usage

#         if useLinkPrefixExtension:
#             m = e2.match(e2)
#             if m:
#                 prefix = m.group(2)
#                 s = m.group(1)
#             else:
#                 prefix = ''
#             # first link
#             if first_prefix:
#                 prefix = first_prefix
#                 first_prefix = False

#         might_be_img = False

#         m = e1.match(line)
#         if m: # page with normal label or alt
#             label = m.group(2)
#             # If we get a ] at the beginning of m.group(3) that means we have a link that is something like:
#             # [[Image:Foo.jpg|[http://example.com desc]]] <- having three ] in a row fucks up,
#             # the real problem is with the e1 regex
#             # See bug 1300.
#             #
#             # Still some problems for cases where the ] is meant to be outside punctuation,
#             # and no image is in sight. See bug 2095.
#             #
#             if label and m.group(3)[0] == ']' and '[' in label:
#                 label += ']' # so that replaceExternalLinks(label) works later
#                 m.group(3) = m.group(3)[1:]
#             # fix up urlencoded title texts
#             if '%' in m.group(1):
#                 # Should anchors '#' also be rejected?
#                 m.group(1) = str_replace(array('<', '>'), array('&lt', '&gt'), rawurldecode(m.group(1)))
#             trail = m.group(3)
#         else:
#             m = e1_img.match(line):
#             if m:
#                 # Invalid, but might be an image with a link in its caption
#                 might_be_img = true
#                 label = m.group(2)
#                 if '%' in m.group(1):
#                     m.group(1) = rawurldecode(m.group(1))
#                 trail = ""
#             else:     # Invalid form; output directly
#                 s += prefix + '[[' + line
#                 continue

#         origLink = m.group(1)

#         # Dont allow internal links to pages containing
#         # PROTO: where PROTO is a valid URL protocol these
#         # should be external links.
#         if (preg_match('/^(?i:' + self.mUrlProtocols + ')/', origLink)) {
#             s += prefix + '[[' + line
#             continue
#         }

#         # Make subpage if necessary
#         if useSubpages:
#             link = self.maybeDoSubpageLink(origLink, label)
#         else:
#             link = origLink

#         noforce = origLink[0] != ':'
#         if not noforce:
#             # Strip off leading ':'
#             link = link[1:]

#         nt = Title::newFromText(self.mStripState.unstripNoWiki(link))
#         if nt is None:
#             s += prefix + '[[' + line
#             continue

#         ns = nt.getNamespace()
#         iw = nt.getInterwiki()

#         if might_be_img { # if this is actually an invalid link
#             if (ns == NS_FILE and noforce) { # but might be an image
#                 found = False
#                 while True:
#                     # look at the next 'line' to see if we can close it there
#                     next_line = iterBrakets.next()
#                     if not next_line:
#                         break
#                     m = explode(']]', next_line, 3)
#                     if m.lastindex == 3:
#                         # the first ]] closes the inner link, the second the image
#                         found = True
#                         label += "[[%s]]%s" % (m.group(0), m.group(1))
#                         trail = m.group(2)
#                         break
#                     elif m.lastindex == 2:
#                         # if there is exactly one ]] that is fine, we will keep looking
#                         label += "[[{m[0]}]]{m.group(1)}"
#                     else:
#                         # if next_line is invalid too, we need look no further
#                         label += '[[' + next_line
#                         break
#                 if not found:
#                     # we couldnt find the end of this imageLink, so output it raw
#                     # but dont ignore what might be perfectly normal links in the text we ve examined
#                     holders.merge(self.replaceInternalLinks2(label))
#                     s += "{prefix}[[%s|%s" % (link, text)
#                     # note: no trail, because without an end, there *is* no trail
#                     continue
#             } else: # it is not an image, so output it raw
#                 s += "{prefix}[[%s|%s" % (link, text)
#                 # note: no trail, because without an end, there *is* no trail
#                      continue
#         }

#         wasblank = (text == '')
#         if wasblank:
#             text = link
#         else:
#             # Bug 4598 madness.  Handle the quotes only if they come from the alternate part
#             # [[Lista d''e paise d''o munno]] . <a href="...">Lista d''e paise d''o munno</a>
#             # [[Criticism of Harry Potter|Criticism of ''Harry Potter'']]
#             #    . <a href="Criticism of Harry Potter">Criticism of <i>Harry Potter</i></a>
#             text = self.doQuotes(text)

#         # Link not escaped by : , create the various objects
#         if noforce and not nt.wasLocalInterwiki():
#             # Interwikis
#             if iw and mOptions.getInterwikiMagic() and nottalk and (
#                     Language::fetchLanguageName(iw, None, 'mw') or
#                     in_array(iw, wgExtraInterlanguageLinkPrefixes)):
#                 # Bug 24502: filter duplicates
#                 if iw not in mLangLinkLanguages:
#                     self.mLangLinkLanguages[iw] = True
#                     self.mOutput.addLanguageLink(nt.getFullText())

#                 s = rstrip(s + prefix)
#                 s += strip(trail, "\n") == '' ? '': prefix + trail
#                 continue

#             if ns == NS_FILE:
#                 if not wfIsBadImage(nt.getDBkey(), self.mTitle):
#                     if wasblank:
#                         # if no parameters were passed, text
#                         # becomes something like "File:Foo.png",
#                         # which we dont want to pass on to the
#                         # image generator
#                         text = ''
#                     else:
#                         # recursively parse links inside the image caption
#                         # actually, this will parse them in any other parameters, too,
#                         # but it might be hard to fix that, and it doesnt matter ATM
#                         text = self.replaceExternalLinks(text)
#                         holders.merge(self.replaceInternalLinks2(text))
#                     # cloak any absolute URLs inside the image markup, so replaceExternalLinks() wont touch them
#                     s += prefix + self.armorLinks(
#                         self.makeImage(nt, text, holders)) + trail
#                 else:
#                     s += prefix + trail
#                 continue

#             if ns == NS_CATEGORY:
#                 s = rstrip(s + "\n") # bug 87

#                 if wasblank:
#                     sortkey = self.getDefaultSort()
#                 else:
#                     sortkey = text
#                 sortkey = Sanitizer::decodeCharReferences(sortkey)
#                 sortkey = str_replace("\n", '', sortkey)
#                 sortkey = self.getConverterLanguage().convertCategoryKey(sortkey)
#                 self.mOutput.addCategory(nt.getDBkey(), sortkey)

#                 s += strip(prefix + trail, "\n") == '' ? '' : prefix + trail

#                 continue
#             }
#         }

#         # Self-link checking. For some languages, variants of the title are checked in
#         # LinkHolderArray::doVariants() to allow batching the existence checks necessary
#         # for linking to a different variant.
#         if ns != NS_SPECIAL and nt.equals(self.mTitle) and !nt.hasFragment():
#             s += prefix + Linker::makeSelfLinkObj(nt, text, '', trail)
#                  continue

#         # NS_MEDIA is a pseudo-namespace for linking directly to a file
#         # @todo FIXME: Should do batch file existence checks, see comment below
#         if ns == NS_MEDIA:
#             # Give extensions a chance to select the file revision for us
#             options = []
#             descQuery = False
#             Hooks::run('BeforeParserFetchFileAndTitle',
#                        [this, nt, &options, &descQuery])
#             # Fetch and register the file (file title may be different via hooks)
#             file, nt = self.fetchFileAndTitle(nt, options)
#             # Cloak with NOPARSE to avoid replacement in replaceExternalLinks
#             s += prefix + self.armorLinks(
#                 Linker::makeMediaLinkFile(nt, file, text)) + trail
#             continue

#         # Some titles, such as valid special pages or files in foreign repos, should
#         # be shown as bluelinks even though they are not included in the page table
#         #
#         # @todo FIXME: isAlwaysKnown() can be expensive for file links; we should really do
#         # batch file existence checks for NS_FILE and NS_MEDIA
#         if iw == '' and nt.isAlwaysKnown():
#             self.mOutput.addLink(nt)
#             s += self.makeKnownLinkHolder(nt, text, array(), trail, prefix)
#         else:
#             # Links will be added to the output link list after checking
#             s += holders.makeHolder(nt, text, array(), trail, prefix)
#     }
#     return holders


def makeInternalLink(title, label):
    colon = title.find(':')
    if colon > 0 and title[:colon] not in options.acceptedNamespaces:
        return ''
    if colon == 0:
        # drop also :File:
        colon2 = title.find(':', colon + 1)
        if colon2 > 1 and title[colon + 1:colon2] not in options.acceptedNamespaces:
            return ''
    if options.keepLinks:
        return '<a href="%s">%s</a>' % (quote(title.encode('utf-8')), label)
    else:
        return label


# ----------------------------------------------------------------------
# External links

# from: https://doc.wikimedia.org/mediawiki-core/master/php/DefaultSettings_8php_source.html

wgUrlProtocols = [
    'bitcoin:', 'ftp://', 'ftps://', 'geo:', 'git://', 'gopher://', 'http://',
    'https://', 'irc://', 'ircs://', 'magnet:', 'mailto:', 'mms://', 'news:',
    'nntp://', 'redis://', 'sftp://', 'sip:', 'sips:', 'sms:', 'ssh://',
    'svn://', 'tel:', 'telnet://', 'urn:', 'worldwind://', 'xmpp:', '//'
]

# from: https://doc.wikimedia.org/mediawiki-core/master/php/Parser_8php_source.html

# Constants needed for external link processing
# Everything except bracket, space, or control characters
# \p{Zs} is unicode 'separator, space' category. It covers the space 0x20
# as well as U+3000 is IDEOGRAPHIC SPACE for bug 19052
EXT_LINK_URL_CLASS = r'[^][<>"\x00-\x20\x7F\s]'
ANCHOR_CLASS = r'[^][\x00-\x08\x0a-\x1F]'
ExtLinkBracketedRegex = re.compile(
    '\[(((?i)' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)' +
    r'\s*((?:' + ANCHOR_CLASS + r'|\[\[' + ANCHOR_CLASS + r'+\]\])' + r'*?)\]',
    re.S | re.U)
# A simpler alternative:
# ExtLinkBracketedRegex = re.compile(r'\[(.*?)\](?!])')

EXT_IMAGE_REGEX = re.compile(
    r"""^(http://|https://)([^][<>"\x00-\x20\x7F\s]+)
    /([A-Za-z0-9_.,~%\-+&;#*?!=()@\x80-\xFF]+)\.((?i)gif|png|jpg|jpeg)$""",
    re.X | re.S | re.U)


def replaceExternalLinks(text):
    """
    https://www.mediawiki.org/wiki/Help:Links#External_links
    [URL anchor text]
    """
    s = ''
    cur = 0
    for m in ExtLinkBracketedRegex.finditer(text):
        s += text[cur:m.start()]
        cur = m.end()

        url = m.group(1)
        label = m.group(3)

        # # The characters '<' and '>' (which were escaped by
        # # removeHTMLtags()) should not be included in
        # # URLs, per RFC 2396.
        # m2 = re.search('&(lt|gt);', url)
        # if m2:
        #     link = url[m2.end():] + ' ' + link
        #     url = url[0:m2.end()]

        # If the link text is an image URL, replace it with an <img> tag
        # This happened by accident in the original parser, but some people used it extensively
        m = EXT_IMAGE_REGEX.match(label)
        if m:
            label = makeExternalImage(label)

        # Use the encoded URL
        # This means that users can paste URLs directly into the text
        # Funny characters like ö aren't valid in URLs anyway
        # This was changed in August 2004
        s += makeExternalLink(url, label)  # + trail

    return s + text[cur:]


def makeExternalLink(url, anchor):
    """Function applied to wikiLinks"""
    if options.keepLinks:
        return '<a href="%s">%s</a>' % (quote(url.encode('utf-8')), anchor)
    else:
        return anchor


def makeExternalImage(url, alt=''):
    if options.keepLinks:
        return '<img src="%s" alt="%s">' % (url, alt)
    else:
        return alt


# ----------------------------------------------------------------------

# match tail after wikilink
tailRE = re.compile('\w+')

syntaxhighlight = re.compile('&lt;syntaxhighlight .*?&gt;(.*?)&lt;/syntaxhighlight&gt;', re.DOTALL)

# skip level 1, it is page name level
section = re.compile(r'(==+)\s*(.*?)\s*\1')

listOpen = {'*': '<ul>', '#': '<ol>', ';': '<dl>', ':': '<dl>'}
listClose = {'*': '</ul>', '#': '</ol>', ';': '</dl>', ':': '</dl>'}
listItem = {'*': '<li>%s</li>', '#': '<li>%s</<li>', ';': '<dt>%s</dt>',
            ':': '<dd>%s</dd>'}


def compact(text):
    """Deal with headers, lists, empty sections, residuals of tables.
    :param text: convert to HTML.
    """

    page = []             # list of paragraph
    headers = {}          # Headers for unfilled sections
    emptySection = False  # empty sections are discarded
    listLevel = []        # nesting of lists
    listCount = []        # count of each list (it should be always in the same length of listLevel)
    for line in text.split('\n'):
        if not line:            # collapse empty lines
            # if there is an opening list, close it if we see an empty line
            if len(listLevel):
                page.append(line)
                if options.toHTML:
                    for c in reversed(listLevel):
                        page.append(listClose[c])
                listLevel = []
                listCount = []
                emptySection = False
            elif page and page[-1]:
                page.append('')
            continue
        # Handle section titles
        m = section.match(line)
        if m:
            title = m.group(2)
            lev = len(m.group(1)) # header level
            if options.toHTML:
                page.append("<h%d>%s</h%d>" % (lev, title, lev))
            if title and title[-1] not in '!?':
                title += '.'    # terminate sentence.
            headers[lev] = title
            # drop previous headers
            for i in list(headers.keys()):
                if i > lev:
                    del headers[i]
            emptySection = True
            listLevel = []
            listCount = []
            continue
        # Handle page title
        elif line.startswith('++'):
            title = line[2:-2]
            if title:
                if title[-1] not in '!?':
                    title += '.'
                page.append(title)
        # handle indents
        elif line[0] == ':':
            # page.append(line.lstrip(':*#;'))
            continue
        # handle lists
        elif line[0] in '*#;:':
            i = 0
            # c: current level char
            # n: next level char
            for c, n in zip_longest(listLevel, line, fillvalue=''):
                if not n or n not in '*#;:': # shorter or different
                    if c:
                        if options.toHTML:
                            page.append(listClose[c])
                        listLevel = listLevel[:-1]
                        listCount = listCount[:-1]
                        continue
                    else:
                        break
                # n != ''
                if c != n and (not c or (c not in ';:' and n not in ';:')):
                    if c:
                        # close level
                        if options.toHTML:
                            page.append(listClose[c])
                        listLevel = listLevel[:-1]
                        listCount = listCount[:-1]
                    listLevel += n
                    listCount.append(0)
                    if options.toHTML:
                        page.append(listOpen[n])
                i += 1
            n = line[i - 1]  # last list char
            line = line[i:].strip()
            if line:  # FIXME: n is '"'
                if options.keepLists:
                    if options.keepSections:
                        # emit open sections
                        items = sorted(headers.items())
                        for _, v in items:
                            page.append(v)
                    headers.clear()
                    # use item count for #-lines
                    listCount[i - 1] += 1
                    bullet = '%d. ' % listCount[i - 1] if n == '#' else '- '
                    page.append('{0:{1}s}'.format(bullet, len(listLevel)) + line)
                elif options.toHTML:
                    page.append(listItem[n] % line)
        elif len(listLevel):
            if options.toHTML:
                for c in reversed(listLevel):
                    page.append(listClose[c])
            listLevel = []
            listCount = []
            page.append(line)

        # Drop residuals of lists
        elif line[0] in '{|' or line[-1] == '}':
            continue
        # Drop irrelevant lines
        elif (line[0] == '(' and line[-1] == ')') or line.strip('.-') == '':
            continue
        elif len(headers):
            if options.keepSections:
                items = sorted(headers.items())
                for i, v in items:
                    page.append(v)
            headers.clear()
            page.append(line)  # first line
            emptySection = False
        elif not emptySection:
            # Drop preformatted
            if line[0] != ' ':  # dangerous
                page.append(line)
    return page


def handle_unicode(entity):
    numeric_code = int(entity[2:-1])
    if numeric_code >= 0x10000: return ''
    return chr(numeric_code)


# ------------------------------------------------------------------------------
# Output


class NextFile(object):
    """
    Synchronous generation of next available file name.
    """

    filesPerDir = 100

    def __init__(self, path_name):
        self.path_name = path_name
        self.dir_index = -1
        self.file_index = -1

    def __next__(self):
        self.file_index = (self.file_index + 1) % NextFile.filesPerDir
        if self.file_index == 0:
            self.dir_index += 1
        dirname = self._dirname()
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        return self._filepath()

    next = __next__

    def _dirname(self):
        char1 = self.dir_index % 26
        char2 = self.dir_index // 26 % 26
        return os.path.join(self.path_name, '%c%c' % (ord('A') + char2, ord('A') + char1))

    def _filepath(self):
        return '%s/wiki_%02d' % (self._dirname(), self.file_index)


class OutputSplitter(object):
    """
    File-like object, that splits output to multiple files of a given max size.
    """

    def __init__(self, nextFile, max_file_size=0, compress=True):
        """
        :param nextFile: a NextFile object from which to obtain filenames
            to use.
        :param max_file_size: the maximum size of each file.
        :para compress: whether to write data with bzip compression.
        """
        self.nextFile = nextFile
        self.compress = compress
        self.max_file_size = max_file_size
        self.file = self.open(next(self.nextFile))

    def reserve(self, size):
        if self.file.tell() + size > self.max_file_size:
            self.close()
            self.file = self.open(next(self.nextFile))

    def write(self, data):
        self.reserve(len(data))
        self.file.write(data)

    def close(self):
        self.file.close()

    def open(self, filename):
        if self.compress:
            return bz2.BZ2File(filename + '.bz2', 'w')
        else:
            return open(filename, 'wb')


# ----------------------------------------------------------------------
# READER

tagRE = re.compile(r'(.*?)<(/?\w+)[^>]*?>(?:([^<]*)(<.*?>)?)?')
#                    1     2               3      4
keyRE = re.compile(r'key="(\d*)"')

def load_templates(file, output_file=None):
    """
    Load templates from :param file:.
    :param output_file: file where to save templates and modules.
    """
    options.templatePrefix = options.templateNamespace + ':'
    options.modulePrefix = options.moduleNamespace + ':'

    if output_file:
        output = codecs.open(output_file, 'wb', 'utf-8')
    for page_count, page_data in enumerate(pages_from(file)):
        id, revid, title, ns, page = page_data
        if not output_file and (not options.templateNamespace or
                                not options.moduleNamespace):  # do not know it yet
            # reconstruct templateNamespace and moduleNamespace from the first title
            if ns in templateKeys:
                colon = title.find(':')
                if colon > 1:
                    if ns == '10':
                        options.templateNamespace = title[:colon]
                        options.templatePrefix = title[:colon + 1]
                    elif ns == '828':
                        options.moduleNamespace = title[:colon]
                        options.modulePrefix = title[:colon + 1]
        if ns in templateKeys:
            text = ''.join(page)
            define_template(title, text)
            # save templates and modules to file
            if output_file:
                output.write('<page>\n')
                output.write('   <title>%s</title>\n' % title)
                output.write('   <ns>%s</ns>\n' % ns)
                output.write('   <id>%s</id>\n' % id)
                output.write('   <text>')
                for line in page:
                    output.write(line)
                output.write('   </text>\n')
                output.write('</page>\n')
        if page_count and page_count % 100000 == 0:
            logging.info("Preprocessed %d pages", page_count)
    if output_file:
        output.close()
        logging.info("Saved %d templates to '%s'", len(options.templates), output_file)


def pages_from(input):
    tagRE = re.compile(r'(.*?)<(/?\w+)[^>]*?>(?:([^<]*)(<.*?>)?)?')
    """
    Scans input extracting pages.
    :return: (id, revid, title, namespace key, page), page is a list of lines.
    """
    # we collect individual lines, since str.join() is significantly faster
    # than concatenation
    revisions = []
    page = []
    id = None
    ns = '0'
    last_id = None
    revid = None
    inText = False
    title = None
    revision_count = 0
    for line in input:
        if '<' not in line:  # faster than doing re.search()
            if inText:
                page.append(line)
            continue
        m = tagRE.search(line)
        if not m:
            continue
        tag = m.group(2)
        if tag == 'page':
            page = []
            redirect = False
        elif tag == 'id' and not id:
            id = m.group(3)
        elif tag == 'id' and id:
            revid = m.group(3)
        elif tag == 'title':
            title = m.group(3)
        elif tag == 'ns':
            ns = m.group(3)
        elif tag == 'redirect':
            redirect = True
        elif tag == 'text':
            if m.lastindex == 3 and line[m.start(3)-2] == '/': # self closing
                # <text xml:space="preserve" />
                continue
            inText = True
            line = line[m.start(3):m.end(3)]
            page.append(line)
            if m.lastindex == 4:  # open-close
                inText = False
        elif tag == '/text':
            if m.group(1):
                page.append(m.group(1))
            inText = False
            revisions.append(page)
            page = []
        elif inText:
            page.append(line)
        elif tag == '/page':
            if id != last_id and not redirect:
                yield (id, revid, title, ns, revisions)
                last_id = id
                ns = '0'
            id = None
            revid = None
            title = None
            page = []
            revisions = []


def process_dump(input_file, template_file, out_file, file_size, file_compress,
                 process_count):
    """
    :param input_file: name of the wikipedia dump file; '-' to read from stdin
    :param template_file: optional file with template definitions.
    :param out_file: directory where to store extracted data, or '-' for stdout
    :param file_size: max size of each extracted file, or None for no max (one file)
    :param file_compress: whether to compress files with bzip.
    :param process_count: number of extraction processes to spawn.
    """

    if input_file == '-':
        input = sys.stdin
    else:
        input = fileinput.FileInput(input_file, openhook=fileinput.hook_compressed)

    # collect siteinfo
    for line in input:
        # When an input file is .bz2 or .gz, line can be a bytes even in Python 3.
        if not isinstance(line, text_type): line = line.decode('utf-8')
        m = tagRE.search(line)
        if not m:
            continue
        tag = m.group(2)
        if tag == 'base':
            # discover urlbase from the xml dump file
            # /mediawiki/siteinfo/base
            base = m.group(3)
            options.urlbase = base[:base.rfind("/")]
        elif tag == 'namespace':
            mk = keyRE.search(line)
            if mk:
                nsid = mk.group(1)
            else:
                nsid = ''
            options.knownNamespaces[m.group(3)] = nsid
            if re.search('key="10"', line):
                options.templateNamespace = m.group(3)
                options.templatePrefix = options.templateNamespace + ':'
            elif re.search('key="828"', line):
                options.moduleNamespace = m.group(3)
                options.modulePrefix = options.moduleNamespace + ':'
        elif tag == '/siteinfo':
            break

    if options.expand_templates:
        # preprocess
        template_load_start = default_timer()
        if template_file:
            if os.path.exists(template_file):
                logging.info("Loading template definitions from: %s", template_file)
                # can't use with here:
                file = fileinput.FileInput(template_file,
                                           openhook=fileinput.hook_compressed)
                load_templates(file)
                file.close()
            else:
                if input_file == '-':
                    # can't scan then reset stdin; must error w/ suggestion to specify template_file
                    raise ValueError("to use templates with stdin dump, must supply explicit template-file")
                logging.info("Preprocessing '%s' to collect template definitions: this may take some time.", input_file)
                load_templates(input, template_file)
                input.close()
                input = fileinput.FileInput(input_file, openhook=fileinput.hook_compressed)
        template_load_elapsed = default_timer() - template_load_start
        logging.info("Loaded %d templates in %.1fs", len(options.templates), template_load_elapsed)

    # process pages
    logging.info("Starting page extraction from %s.", input_file)
    extract_start = default_timer()

    # Parallel Map/Reduce:
    # - pages to be processed are dispatched to workers
    # - a reduce process collects the results, sort them and print them.

    process_count = max(1, process_count)
    maxsize = 10 * process_count
    # output queue
    output_queue = Queue(maxsize=maxsize)

    if out_file == '-':
        out_file = None

    worker_count = process_count

    # load balancing
    max_spool_length = 10000
    spool_length = Value('i', 0, lock=False)

    # reduce job that sorts and prints output
    reduce = Process(target=reduce_process,
                     args=(options, output_queue, spool_length,
                           out_file, file_size, file_compress))
    reduce.start()

    # initialize jobs queue
    jobs_queue = Queue(maxsize=maxsize)

    # start worker processes
    logging.info("Using %d extract processes.", worker_count)
    workers = []
    for i in range(worker_count):
        extractor = Process(target=extract_process,
                            args=(options, i, jobs_queue, output_queue))
        extractor.daemon = True  # only live while parent process lives
        extractor.start()
        workers.append(extractor)

    # Mapper process
    page_num = 0
    for page_data in pages_from(input):
        id, revid, title, ns, page = page_data
        if keepPage(ns, page):
            # slow down
            delay = 0
            if spool_length.value > max_spool_length:
                # reduce to 10%
                while spool_length.value > max_spool_length/10:
                    time.sleep(10)
                    delay += 10
            if delay:
                logging.info('Delay %ds', delay)
            job = (id, revid, title, page, page_num)
            jobs_queue.put(job) # goes to any available extract_process
            page_num += 1
        page = None             # free memory

    input.close()

    # signal termination
    for _ in workers:
        jobs_queue.put(None)
    # wait for workers to terminate
    for w in workers:
        w.join()

    # signal end of work to reduce process
    output_queue.put(None)
    # wait for it to finish
    reduce.join()

    extract_duration = default_timer() - extract_start
    extract_rate = page_num / extract_duration
    logging.info("Finished %d-process extraction of %d articles in %.1fs (%.1f art/s)",
                 process_count, page_num, extract_duration, extract_rate)


# ----------------------------------------------------------------------
# Multiprocess support


def extract_process(opts, i, jobs_queue, output_queue):
    """Pull tuples of raw page content, do CPU/regex-heavy fixup, push finished text
    :param i: process id.
    :param jobs_queue: where to get jobs.
    :param output_queue: where to queue extracted text for output.
    """

    global options
    options = opts

    createLogger(options.quiet, options.debug)

    out = StringIO()                 # memory buffer
    
    
    while True:
        job = jobs_queue.get()  # job is (id, title, page, page_num)
        if job:
            id, revid, title, page, page_num = job
            try:
                e = Extractor(*job[:4]) # (id, revid, title, page)
                page = None              # free memory
                e.extract(out)
                text = out.getvalue()
            except:
                text = ''
                logging.exception('Processing page: %s %s', id, title)

            output_queue.put((page_num, text))
            out.truncate(0)
            out.seek(0)
        else:
            logging.debug('Quit extractor')
            break
    out.close()


report_period = 10000           # progress report period
def reduce_process(opts, output_queue, spool_length,
                   out_file=None, file_size=0, file_compress=True):
    """Pull finished article text, write series of files (or stdout)
    :param opts: global parameters.
    :param output_queue: text to be output.
    :param spool_length: spool length.
    :param out_file: filename where to print.
    :param file_size: max file size.
    :param file_compress: whether to compress output.
    """

    global options
    options = opts
    
    createLogger(options.quiet, options.debug)
    
    if out_file:
        nextFile = NextFile(out_file)
        output = OutputSplitter(nextFile, file_size, file_compress)
    else:
        output = sys.stdout if PY2 else sys.stdout.buffer
        if file_compress:
            logging.warn("writing to stdout, so no output compression (use an external tool)")

    interval_start = default_timer()
    # FIXME: use a heap
    spool = {}        # collected pages
    next_page = 0     # sequence numbering of page
    while True:
        if next_page in spool:
            output.write(spool.pop(next_page).encode('utf-8'))
            next_page += 1
            # tell mapper our load:
            spool_length.value = len(spool)
            # progress report
            if next_page % report_period == 0:
                interval_rate = report_period / (default_timer() - interval_start)
                logging.info("Extracted %d articles (%.1f art/s)",
                             next_page, interval_rate)
                interval_start = default_timer()
        else:
            # mapper puts None to signal finish
            pair = output_queue.get()
            if not pair:
                break
            page_num, text = pair
            spool[page_num] = text
            # tell mapper our load:
            spool_length.value = len(spool)
            # FIXME: if an extractor dies, process stalls; the other processes
            # continue to produce pairs, filling up memory.
            if len(spool) > 200:
                logging.debug('Collected %d, waiting: %d, %d', len(spool),
                              next_page, next_page == page_num)
    if output != sys.stdout:
        output.close()


# ----------------------------------------------------------------------

# Minimum size of output files
minFileSize = 200 * 1024

def main():

    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)
    parser.add_argument("input",
                        help="XML wiki dump file")
    groupO = parser.add_argument_group('Output')
    groupO.add_argument("-o", "--output", default="text",
                        help="directory for extracted files (or '-' for dumping to stdout)")
    groupO.add_argument("-b", "--bytes", default="1M",
                        help="maximum bytes per output file (default %(default)s)",
                        metavar="n[KMG]")
    groupO.add_argument("-c", "--compress", action="store_true",
                        help="compress output files using bzip")
    groupO.add_argument("--json", action="store_true",
                        help="write output in json format instead of the default one")


    groupP = parser.add_argument_group('Processing')
    groupP.add_argument("--html", action="store_true",
                        help="produce HTML output, subsumes --links")
    groupP.add_argument("-l", "--links", action="store_true",
                        help="preserve links")
    groupP.add_argument("-s", "--sections", action="store_true",
                        help="preserve sections")
    groupP.add_argument("--lists", action="store_true",
                        help="preserve lists")
    groupP.add_argument("-ns", "--namespaces", default="", metavar="ns1,ns2",
                        help="accepted namespaces in links")
    groupP.add_argument("--templates",
                        help="use or create file containing templates")
    groupP.add_argument("--no-templates", action="store_false",
                        help="Do not expand templates")
    groupP.add_argument("-r", "--revision", action="store_true", default=options.print_revision,
                        help="Include the document revision id (default=%(default)s)")
    groupP.add_argument("--min_text_length", type=int, default=options.min_text_length,
                        help="Minimum expanded text length required to write document (default=%(default)s)")
    groupP.add_argument("--filter_disambig_pages", action="store_true", default=options.filter_disambig_pages,
                        help="Remove pages from output that contain disabmiguation markup (default=%(default)s)")
    groupP.add_argument("-it", "--ignored_tags", default="", metavar="abbr,b,big",
                        help="comma separated list of tags that will be dropped, keeping their content")
    groupP.add_argument("-de", "--discard_elements", default="", metavar="gallery,timeline,noinclude",
                        help="comma separated list of elements that will be removed from the article text")
    groupP.add_argument("--keep_tables", action="store_true", default=options.keep_tables,
                        help="Preserve tables in the output article text (default=%(default)s)")
    default_process_count = max(1, cpu_count() - 1)
    parser.add_argument("--processes", type=int, default=default_process_count,
                        help="Number of processes to use (default %(default)s)")

    groupS = parser.add_argument_group('Special')
    groupS.add_argument("-q", "--quiet", action="store_true",
                        help="suppress reporting progress info")
    groupS.add_argument("--debug", action="store_true",
                        help="print debug info")
    groupS.add_argument("-a", "--article", action="store_true",
                        help="analyze a file containing a single article (debug option)")
    groupS.add_argument("-v", "--version", action="version",
                        version='%(prog)s ' + version,
                        help="print program version")

    args = parser.parse_args()

    options.keepLinks = args.links
    options.keepSections = args.sections
    options.keepLists = args.lists
    options.toHTML = args.html
    options.write_json = args.json
    options.print_revision = args.revision
    options.min_text_length = args.min_text_length
    if args.html:
        options.keepLinks = True

    options.expand_templates = args.no_templates
    options.filter_disambig_pages = args.filter_disambig_pages
    options.keep_tables = args.keep_tables

    try:
        power = 'kmg'.find(args.bytes[-1].lower()) + 1
        file_size = int(args.bytes[:-1]) * 1024 ** power
        if file_size < minFileSize:
            raise ValueError()
    except ValueError:
        logging.error('Insufficient or invalid size: %s', args.bytes)
        return

    if args.namespaces:
        options.acceptedNamespaces = set(args.namespaces.split(','))

    # ignoredTags and discardElemets have default values already supplied, if passed in the defaults are overwritten
    if args.ignored_tags:
        ignoredTags = set(args.ignored_tags.split(','))
    else:
        ignoredTags = [
            'abbr', 'b', 'big', 'blockquote', 'center', 'cite', 'em',
            'font', 'h1', 'h2', 'h3', 'h4', 'hiero', 'i', 'kbd',
            'p', 'plaintext', 's', 'span', 'strike', 'strong',
            'tt', 'u', 'var'
        ]

    # 'a' tag is handled separately
    for tag in ignoredTags:
        ignoreTag(tag)

    if args.discard_elements:
        options.discardElements = set(args.discard_elements.split(','))

    FORMAT = '%(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT)

    options.quiet = args.quiet
    options.debug = args.debug
    
    createLogger(options.quiet, options.debug)

    input_file = args.input

    if not options.keepLinks:
        ignoreTag('a')

    # sharing cache of parser templates is too slow:
    # manager = Manager()
    # templateCache = manager.dict()

    if args.article:
        if args.templates:
            if os.path.exists(args.templates):
                with open(args.templates) as file:
                    load_templates(file)

        file = fileinput.FileInput(input_file, openhook=fileinput.hook_compressed)
        for page_data in pages_from(file):
            id, revid, title, ns, page = page_data
            Extractor(id, revid, title, page).extract(sys.stdout)
        file.close()
        return

    output_path = args.output
    if output_path != '-' and not os.path.isdir(output_path):
        try:
            os.makedirs(output_path)
        except:
            logging.error('Could not create: %s', output_path)
            return

    process_dump(input_file, args.templates, output_path, file_size,
                 args.compress, args.processes)

def createLogger(quiet, debug):
    logger = logging.getLogger()
    if not quiet:
        logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    main()