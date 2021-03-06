# Local Zendesk Help Center

Back your Zendesk Help Center in git. Modify articles locally, and deploy
directly to Zendesk.

Goals of this project:

- Back Help Center locally (via git), not Zendesk
- Give revision control of articles
- Reviewing article edits/changes made simpler
- Platform flexibility to be able to switch away from Zendesk

**Note: Images will be backed by Amazon S3 so you will need an AWS account
for the images to no longer be owned by Zendesk. Otherwise, you can leave
images backed on Zendesk and comment out all scripts that involve S3.**

## Prerequisites

- Python 2.7

- Add environment variables: 
    - Cloudfront URL: `ZENDESK_CLOUDFRONT_URL`
    - Zendesk subdomain: `ZENDESK_SUBDOMAIN`
	- Zendesk agent username: `ZENDESK_USR`
	- Zendesk agent password: `ZENDESK_PWD`
	- Zendesk AWS bucket name: `ZENDESK_BUCKET_NAME`
	- AWS Access Key: `AWS_ACCESS_KEY`
	- AWS Secret Key: `AWS_SECRET_KEY`

## Installation
Run `pip install zendesk-help-center-backer`

## Usage

###Tracking Changes

Before locally editing articles and images, **always run `zendesk-track`**.
This allows for local viewing of content. All local content is available in the
"out" folder. To quit `zendesk-track`, type CTRL+C.

### Creating New Articles

- Run `zendesk-new` with a Zendesk Section ID as the parameter.
- Add the title to the file `title.html`.
- Open the file `index.html` and write the article.
	- For images, enter: `img src="<image_name>"` with the
      appropriate file type at the end (png, jpg, jpeg, gif).
	- For links to other articles, enter: `a href="<article_id>"` with the ID
      of the article you want to link to inserted.

### Local Viewing

- Ensure `zendesk-track` is running. If it wasn't, run it now.
- Once the article is complete, open the version of the article in the "out"
  folder for local viewing. This will provide a basic HTML view in your
  preferred browser.

### Deployment

- When you are ready to publish your changes, you have two options:
	- To deploy a single article, run `zendesk-deploy <article_id>`.
    - To deploy all the articles, run `zendesk-deploy` with no parameters.
- Commit all changes that you make in the "posts" folder to GitHub
to ensure revision control and allow others to review your changes.

To edit past articles, simply edit the HTML files with `zendesk-track`
running. Local edits can be viewed in the "out" folder and use `zendesk-deploy` as
outlined above to publish the edits. You must have Zendesk editing capabilities
for the article. The final version should also be commited to GitHub.

## License

BSD 3-Clause, see accompanying LICENSE file.
