name: interactionroom.careerdigitalfair.com

on:
  push:
    branches:
      -  interactionroom.careerdigitalfair.com_Luigi
      
  workflow_dispatch:
      
jobs:
  Deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Git clone
        uses: actions/checkout@v2
        with:
          ref: interactionroom.careerdigitalfair.com_Luigi
        
      - name: copy file via ssh password
        uses: appleboy/scp-action@master
        with:
          host: ${{ secrets.INTERACTIONROOM_HOST }}
          username: ${{ secrets.INTERACTIONROOM_USER }}
          password: ${{ secrets.INTERACTIONROOM_PASS }}
          port: ${{ secrets.INTERACTIONROOM_PORT }}
          source: "Back/s2.py"
          target: "/var/www/stat/stat/"
