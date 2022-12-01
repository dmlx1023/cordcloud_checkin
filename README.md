## Automatic check-in script for CordCloud

This is a script that will automatically check in your CordCloud account and get the traffic every day.

## `Usage`
You have two ways to use this script:

1. Run the script in your machine.  
`python AutoCheckIn.py --username=<username> --password=<password> --cookie=<cookie> [--keep-cookie]`  
`username`: Your CordCloud username.Required.  
`password`: Your CordCloud password.Required.  
`url`: The cordcloud url ( e.g: `https://www.cordc.net` note that you shouldn't add a `/` behind the url).  
***
2. Run the script in Github Actions.(recommended)  
First, fork this repository to your own repository.  
Then update the cron time you want in you Github Actions workflow file.  
And set the `USERNAME` , `PASSWORD` and `URL` in the Github Actions secrets  which are in the repository settings rather than github settings.
`Settings->Secrets->Actions->New repository secret`.  
All done! :smile_cat: :smile_cat: :smile_cat:
***

If you have any question, welcome to post issues!
```yaml
on:
  schedule:
    - cron: '0 16 * * *'
```
