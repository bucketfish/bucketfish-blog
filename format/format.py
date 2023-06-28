
# note to self: actually comment shit. lol

import os
import glob # pattern expression for files
import markdown

import json

# grab the template
with open("format/template.html") as f:
    template = f.read()

# template for index
with open("format/index_template.html") as f:
    index_template = f.read()

index_posts = ""
iposts_format = """
<li>
{{date}} <a href="{{link}}">{{title}}</a>
</li>
"""
# grab the data for sorting later, if needed
# with open('scripts/articles.json') as json_file:
#     article_data = json.load(json_file)

# load up the files that match the place
for f in glob.iglob('markdown_content/*.md'):
    body = ""

    # read the file
    with open(f, 'r') as file:
        raw = file.read()
        lines = raw.split("\n")

        # process each line to check for arguments
        for line in lines:
            stripped = line.lstrip()
            indentation = line[:len(line) - len(stripped)] # help i don't remember what this was for.

            # process arguments
            if stripped.startswith('^'):

                # .partition splits it into three elements, before, the match, and after
                # we don't want the match so we just split it yah
                command,_,args = stripped.rstrip('\n').lstrip('^').partition(' ')
                args = args.strip() # just in case there are extra spaces

                # keep track of args
                if command == 'title':
                    title = args

                elif command == 'section':
                    section = args

                elif command == 'category':
                    category = args
                    """
                    possible categories:
                    - technicality — how tos!
                    - thoughts — recs, whatever i want
                    - artistry — creations, innovations, ideas
                    - journal — irl recaps, learns

                    yay!
                    """

                elif command == 'description':
                    description = args

                elif command == "date":
                    date = args

                elif command == "slug":
                    slug = args

                elif command == "readingtime":
                    readingtime = args

                else:
                    print("UNKNOWN COMMAND:", command, args)

            else:
                # double backslash for formatting. consider changing this to like. different paragraphs. you getz.......
                body += line + "\n\n"

    # this is only to get the index of the article, ie. the 00_, to update json dict
    # we don't need it since we don't care about json
    # file_name = os.path.basename(f)

    # change this part for . location output

    newpath = os.path.join("p", slug.lower())
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    destination = os.path.join("p", slug.lower(), "index.html")

    with open(destination, 'w') as file:
        output = template
        output = output.replace("{{body}}", markdown.markdown(body, extensions=["fenced_code", "codehilite"]))
        output = output.replace("{{title}}", title)
        output = output.replace("{{category}}", category)
        output = output.replace("{{description}}", description)
        output = output.replace("{{date}}", date)
        output = output.replace("{{readingtime}}", readingtime)


        file.write(output)


    curipost = iposts_format
    curipost = curipost.replace("{{link}}", "p/" + slug.lower())
    curipost = curipost.replace("{{title}}", title)
    curipost = curipost.replace("{{date}}", date)

    index_posts += curipost
    # update data json dict
    #
    # if title not in article_data.keys():
    #     article_data[title] = {}
    # article_data[title]["title"] = title
    # article_data[title]["index"] = int(os.path.splitext(file_name)[0].split('_')[0])
    # article_data[title]["tags"] = tags
    #
    #
    # json_string = json.dumps(article_data)
    #
    # with open('scripts/articles.json', 'w') as outfile:
    #     outfile.write(json_string)


# rebuild the main page
destination = "index.html"
with open(destination, 'w') as file:
    index_template = index_template.replace("{{posts}}", index_posts)
    file.write(index_template)
