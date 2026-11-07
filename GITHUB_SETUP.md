# First GitHub upload — ConceptLens

Repository name: `conceptlens`

Display title: **ConceptLens — Understanding Beyond Memorization**

Suggested About description: ConceptLens is a HackCartel education research prototype that explores the difference between recalling an answer and applying a concept.

## Create the empty repository

On GitHub, choose New repository, select the intended HackCartel organization or your account, and use `conceptlens` as the name. Choose the intended visibility. Do not initialize a README, .gitignore, or license: these starter files will be uploaded from your computer.

## Upload with Windows PowerShell

Extract this ZIP. Open a terminal inside the `conceptlens` folder containing `README.md`.
Replace `YOUR-OWNER` below with the exact GitHub organization or username.

```powershell
git init
git branch -M main
git add .
git commit -m "docs: initialize ConceptLens project"
git remote add origin https://github.com/YOUR-OWNER/conceptlens.git
git push -u origin main
```

If Git asks for author identity, configure it and repeat the commit and push:

```powershell
git config user.name "Your Name"
git config user.email "YOUR-GITHUB-EMAIL"
```

Complete GitHub's authentication prompt when pushing. If the repository already contains commits, clone it first and copy these starter files into the clone instead of using the empty-repository procedure. Do not force-push over existing work.

## Invite the group

Add the five members through the repository access settings, or grant access to the appropriate organization team. Members can then clone:

```powershell
git clone https://github.com/YOUR-OWNER/conceptlens.git
cd conceptlens
```

Suggested topics: `hackcartel`, `education`, `learning-analytics`, `python`, `research-prototype`.
