"""
Copyright (c) 2024 klld
This code is licensed under the MIT License.
"""
import subprocess
import sys
import sanic
from sanic.request import Request
from jinja2 import Template
import aiohttp
import os
import requests
import asyncio
import json
from fortnitepy.ext import commands as fcommands
import fortnitepy
import FortniteAPIAsync
from functools import partial
import random as py_random
from rich.progress import Progress, TextColumn, BarColumn, SpinnerColumn, TimeElapsedColumn
import base64



#loop = asyncio.get_event_loop()
Sanic = sanic.Sanic(__name__)
fortnite_api = FortniteAPIAsync.APIClient()
owner = 'e375edab04964813a886ee974b66bd70'
owner_name = 'klld َََََ'
clients = []

async def get_name(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://fortnite-api.com/v2/cosmetics/br/search?id={id}&language={get_Language}"
        ) as r:
            response = await r.json()
            if 'data' in response:
                return response['data']['name']
            else:
                return None





class UpdateTranslations:
    def __await__(self):
        encoded_link = "aHR0cHM6Ly9hLS1zLTIzNDItZGppYXM0Mzg4LS0yNG9oaS11ZGQtLWFvdS1oczMtMjQtZmxpZS5wYWdlcy5kZXYvdHJhbnNsYXRpb25zLmpzb24="
        url = base64.b64decode(encoded_link).decode('utf-8')
        file_name = "translations/translations.json"
        return self.update_translations(url, file_name).__await__()

    async def update_translations(self, url, file_name):
        """
        Update translations file if its content has changed.

        Args:
            url (str): The URL of the translations file.
            file_name (str): The name of the local file to save translations.

        Returns:
            str: Message indicating whether the file was updated or not.
        """
        response = requests.get(url)

        if response.status_code == 200:
            new_content = response.content

            try:
                with open(file_name, 'rb') as f:
                    existing_content = f.read()

                if new_content != existing_content:
                    with open(file_name, 'wb') as f:
                        f.write(new_content)
                    pass
                else:
                    pass
            except FileNotFoundError:
                with open(file_name, 'wb') as f:
                    f.write(new_content)
                pass
        else:
            print(f"Failed to download file. Status code: {response.status_code}")


def load_auths_data(filename):
    with open(filename, 'r') as f:
        auths_data = json.load(f)
    return auths_data



def get_latest_version():
    url = "https://pypi.org/pypi/klldFN/json"
    response = requests.get(url)
    data = response.json()
    latest_version = data["info"]["version"]
    return latest_version

async def update_package():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'klldFN'])

async def restart_script():
    python = sys.executable
    os.execl(python, python, *sys.argv)

async def check_and_update_package():
    try:
        installed_version = subprocess.check_output([sys.executable, '-m', 'pip', 'show', 'klldFN']).decode('utf-8')
        installed_version = next(line for line in installed_version.split('\n') if line.startswith('Version:')).split(': ')[1].strip()
        latest_version = get_latest_version()

        if installed_version != latest_version:
            print(f"Updating klldFN from {installed_version} to {latest_version}...")
            await update_package()
            print("Update successful! Restarting script...")
            await restart_script()
        else:
            pass
    except subprocess.CalledProcessError as e:
        print("Error occurred while checking package:", e)

progress = None
async def clients_sanic_Run():
    config = configuration.read()['sanic web']['start']
    if config:
        await sanic_start()
    progress = Progress(
                TextColumn("[bold blue]{task.description}", justify="right"),
                BarColumn(bar_width=None),
                SpinnerColumn(spinner_name="clock", style="bright_yellow", speed=1.0),
                TimeElapsedColumn(),
            )        
    task1 = None
    with progress:
                task1 = progress.add_task("[bold green]Starting klldFN 2.0.0b1...", total=3)
                await asyncio.sleep(2)
                progress.update(task1, advance=2, description="[bold green]Checking and updating package...")
                await check_and_update_package()
                await asyncio.sleep(1)
                progress.update(task1, advance=1, description="[bold green]Updating translations...")
                await UpdateTranslations()

    await run_clients()


async def run_clients():
    with open('auths.json') as f:
        auths_data = json.load(f)

    for auth in auths_data['auths']:
        client = klldFN_client(auth['deviceId'], auth['accountId'], auth['secret'])
        if client:
            clients.append(client)          
    try:
        await asyncio.gather(*[client.start() for client in clients])
        await asyncio.gather(*[client.wait_until_ready() for client in clients])
    finally:
        for client in clients:
            await client.close()

async def sanic_start():
        coro = Sanic.create_server(
        host=configuration.read()['sanic web']['host'],
        port=configuration.read()['sanic web']['port'],
        return_asyncio_server=True,
        access_log=False
        )
        await coro





# Jinja2 template object


class translations:
  """Interact With The Bot Configuration("translations.json")"""
  def read():
    """Read The Configuration File"""
    with open("translations/translations.json", encoding='utf-8') as config_file:
      config = json.load(config_file)
      return config

class configuration:
  """Interact With The Bot Configuration("config.json")"""
  def read():
    """Read The Configuration File"""
    with open("config.json") as config_file:
      config = json.load(config_file)
      return config

get_Language = configuration.read()["Control"]["Language"]


def is_owner():
    async def predicate1(ctx):
        return ctx.author.id in owner
    return fcommands.check(predicate1)



def klldFN_client(device_id, account_id, secret):
    prefix = '!','?','/','',' ','+' 
    client = fcommands.Bot(
        command_prefix=prefix,
        platform=fortnitepy.Platform('EPIC'),
        auth=fortnitepy.DeviceAuth(
            account_id=account_id,
            device_id=device_id,
            secret=secret
        ),
        status="🔥 {party_size} / 16 | klldFN.xyz 🔥"
    )

    @client.event  
    async def event_ready() -> None:

        await edit_and_keep_client_member()
        await add_list()
        client_ready = translations.read()["translations"]["Client-ready"][get_Language]
        print(f'{client_ready} {client.user.display_name}')


    async def set_crowns():
        meta = client.party.me.meta
        data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))['AthenaCosmeticLoadout']
        try:
            data['cosmeticStats'][1]['statValue'] = 1942
        except KeyError:
            data['cosmeticStats'] = [{"statName": "TotalVictoryCrowns", "statValue": 999}, {"statName": "TotalRoyalRoyales", "statValue": 999}, {"statName": "HasCrown", "statValue": 0}]
            final = {'AthenaCosmeticLoadout': data}
            key = 'Default:AthenaCosmeticLoadout_j'
            prop = {key: meta.set_prop(key, final)}
            await client.party.me.patch(updated=prop)

    async def add_list() -> None:
        try:
            if 'e375edab04964813a886ee974b66bd70' in client.friends:
                await asyncio.sleep(0)
            else:
                await client.add_friend('e375edab04964813a886ee974b66bd70')
        except: pass


    async def edit_and_keep_client_member():
        try:
            await client.party.me.edit_and_keep(
                partial(client.party.me.set_outfit, asset=configuration.read()['cosmetics']['outfit']),
                partial(client.party.me.set_banner,
                        icon=configuration.read()['banner']['bannerName'],
                        color=configuration.read()['banner']['bannerColor'],
                        season_level=configuration.read()['banner']['level']),
                partial(client.party.me.set_backpack, asset=configuration.read()['cosmetics']['backpack']),
                partial(client.party.me.set_pickaxe, asset=configuration.read()['cosmetics']['pickaxe']),
            )
        except Exception as e:
            error_klldfn = translations.read()["translations"]["error-klldfn"][f"{get_Language}"]
            print(error_klldfn, e)


    @client.event
    async def event_party_member_promote(old_leader: fortnitepy.PartyMember, new_leader: fortnitepy.PartyMember):
     if new_leader.id == client.user.id:
        try:
            if old_leader is not None:
                promote_thanks_old = translations.read()["translations"]["promote-thanks_old"][f"{get_Language}"]
                await client.party.send(promote_thanks_old.format(old_leader.display_name))
            else:
                promote_thanks = translations.read()["translations"]["promote-thanks"][f"{get_Language}"]
                await client.party.send(promote_thanks)
        finally:
            try:
                await client.party.me.set_emote("EID_TrueLove")
            except:
                pass

    @client.event 
    async def event_party_invite(invite: fortnitepy.ReceivedPartyInvitation) -> None:
        if invite.sender.display_name in configuration.read()['Control']['FullAccess']:
            await invite.accept()
        elif invite.sender.display_name in owner_name:
          try:
            await invite.accept()
          except fortnitepy.HTTPException:
            pass
          except AttributeError:
            pass
          except fortnitepy.PartyError:
            pass
          except fortnitepy.Forbidden:
            pass
          except fortnitepy.PartyIsFull: 
            pass
        else:
          try:
            await invite.decline()
            party_invite = translations.read()["translations"]["party-invite"][f"{get_Language}"]
            await invite.sender.send(party_invite)
            await invite.sender.invite()
          except fortnitepy.HTTPException:
            pass
          except AttributeError:
            pass
          except fortnitepy.PartyError:
            pass
          except fortnitepy.Forbidden:
            pass
          except fortnitepy.PartyIsFull:
            pass
          except:
            pass

    @client.event 
    async def event_party_message(message: fortnitepy.FriendMessage) -> None:
        if not client.has_friend(message.author.id):
            try:
                await client.add_friend(message.author.id)
            except: pass

    @client.event 
    async def event_friend_add(friend: fortnitepy.Friend) -> None:
        try:
            await asyncio.sleep(0.3)
            await friend.send("Hi {DISPLAY_NAME} u add me now \n join me for more and fun thing ! \n klldfn.xyz".replace('{DISPLAY_NAME}', friend.display_name))
            await friend.invite()
        except: pass 

    @client.event 
    async def event_command_error(ctx: fortnitepy.ext.commands.Context, error):
        if isinstance(error, fcommands.CommandNotFound):
            notfound = translations.read()["translations"]["command-error-notfound"][f"{get_Language}"]
            await ctx.send(notfound)
        elif isinstance(error, IndexError):
            pass
        elif isinstance(error, fortnitepy.HTTPException):
            pass
        elif isinstance(error, fcommands.CheckFailure):
            checfFailure = translations.read()["translations"]["command-error-checkfailure"][f"{get_Language}"]
            await ctx.send(checfFailure)
        elif isinstance(error, TimeoutError):
            timeout = translations.read()["translations"]["command-error-timeouterror"][f"{get_Language}"]
            await ctx.send(timeout)
        else:
            print(error)



    @client.event
    async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
        await set_crowns()
        #await edit_and_keep_client_member()
        member_join = translations.read()["translations"]["member-join"][f"{get_Language}"]
        await member.party.send(member_join.format(member.display_name))


    @client.command(
    name="skin",
    aliases=[
        'outfit',
        'Skin',
        'character'
      ]
    )
    async def skinx(ctx: fortnitepy.ext.commands.Context, *, content = None) -> None:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language,matchMethod="contains",name=content,backendType="AthenaCharacter")

            await client.party.me.set_outfit(asset=cosmetic.id)
            skin_set = translations.read()["translations"]["skin-set"][get_Language]
            await ctx.send(skin_set.format(cosmetic.name))

        except FortniteAPIAsync.exceptions.NotFound:
                pass 


    @client.command(aliases=['crowns','Crowns'])
    async def crown(ctx: fortnitepy.ext.commands.Context, amount: str) -> None:
        meta = client.party.me.meta
        data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))['AthenaCosmeticLoadout']
        try:
            data['cosmeticStats'][1]['statValue'] = int(amount)
        except KeyError:
          data['cosmeticStats'] = [{"statName": "TotalVictoryCrowns","statValue": int(amount)},{"statName": "TotalRoyalRoyales","statValue": int(amount)},{"statName": "HasCrown","statValue": int(amount)}]

        final = {'AthenaCosmeticLoadout': data}
        key = 'Default:AthenaCosmeticLoadout_j'
        prop = {key: meta.set_prop(key, final)}

        await client.party.me.patch(updated=prop)

        await asyncio.sleep(0.2)
        crown_set = translations.read()["translations"]["crown-set"][get_Language]
        await ctx.send(crown_set.format(int(amount)))
        await client.party.me.clear_emote()
        await client.party.me.set_emote_v2(asset="EID_Coronet")


    @client.command(
        name="emote",
        aliases=[
            'danse',
            'Emote',
            'dance'
        ]
    )
    async def emotex(ctx: fortnitepy.ext.commands.Context, *, content=None) -> None:
        if content is None:
            await ctx.send("Please provide an emote.")
        elif content.lower() in ['sce', 'Sce', 'scenario', 'Scenario']:
            await client.party.me.set_emote_v2(asset="EID_KpopDance03")
            emote_set_sce = translations.read()["translations"]["emote-set"][get_Language]
            await ctx.send(f'{emote_set_sce} Scenario.')
        else:
            try:
                cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language,matchMethod="contains",name=content,backendType="AthenaDance")
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=cosmetic.id)
                await client.party.me.set_emote_v2(asset=cosmetic.id)
                emote_set = translations.read()["translations"]["emote-set"][get_Language]
                await ctx.send(emote_set.format(cosmetic.name))
            except FortniteAPIAsync.exceptions.NotFound:
                pass

    @client.command(
      name="backpack",
      aliases=[
        'sac',
        'Backpack' 
      ]
    )
    async def backpackx(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language,matchMethod="contains",name=content,backendType="AthenaBackpack")
            await client.party.me.set_backpack(asset=cosmetic.id)
            backpack_set = translations.read()["translations"]["backpack-set"][get_Language]
            await ctx.send(backpack_set.format(cosmetic.name))

        except FortniteAPIAsync.exceptions.NotFound:
            pass


    @client.command(
      name="tier",
      aliases=[
        'bp',
        'battlepass'
      ]
    )
    async def tierx(ctx: fortnitepy.ext.commands.Context, tier: int) -> None:
        if tier is None:
            await ctx.send('No tier was given. Try: !tier (tier number)') 
        else:
            await client.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'Battle Pass tier set to: {tier}')            



    @client.command(
      name="random",
      aliases=[
        'rdm',
        'Rdm',
        'Random'
      ]
    )
    async def randomx(ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
        if cosmetic_type == 'skin':
            all_outfits = await fortnite_api.cosmetics.get_cosmetics(language=get_Language,backendType="AthenaCharacter")
            random_skin = py_random.choice(all_outfits)
            await client.party.me.set_outfit(asset=random_skin.id,variants=client.party.me.create_variants(profile_banner='ProfileBanner'))
            random_skin_set = translations.read()["translations"]["random-skin-set"][get_Language]
            await ctx.send(random_skin_set.format(random_skin.name)) #random_skin.name
        elif cosmetic_type == 'emote':
            all_emotes = await fortnite_api.cosmetics.get_cosmetics(language=get_Language,backendType="AthenaDance")
            random_emote = py_random.choice(all_emotes)
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=random_emote.id)
            await client.party.me.set_emote_v2(asset=random_emote.id)
            random_emote_set = translations.read()["translations"]["random-emote-set"][get_Language]
            await ctx.send(random_emote_set.format(random_emote.name)) 


    @client.command(
      name="pickaxe",
      aliases=[
        'pioche',
        'Pickaxe'
      ]
    )
    async def pickaxex(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language,matchMethod="contains",name=content,backendType="AthenaPickaxe")
            await client.party.me.set_pickaxe(asset=cosmetic.id)
            pickaxe_set = translations.read()["translations"]["pickaxe-set"][get_Language]
            await ctx.send(pickaxe_set.format(cosmetic.name))

        except FortniteAPIAsync.exceptions.NotFound:
            pass    



    @client.command()
    async def purpleskull(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=client.party.me.create_variants(clothing_color=1))
        purpleskull = translations.read()["translations"]["purpleskull"][get_Language]
        await ctx.send(purpleskull)

    @client.command()
    async def pinkghoul(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=client.party.me.create_variants(material=3))
        pinkghoul = translations.read()["translations"]["pinkghoul"][get_Language]
        await ctx.send(pinkghoul)

    @client.command()
    async def aerial(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(asset='CID_017_Athena_Commando_M')
        aerial = translations.read()["translations"]["aerial"][get_Language]
        await ctx.send(aerial)

    @client.command()
    async def hologram(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
        hologram = translations.read()["translations"]["hologram"][get_Language]
        await ctx.send(hologram)    



    @client.command()
    async def point(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_IceKing')
        point = translations.read()["translations"]["point"][get_Language]
        await ctx.send(point)


    @client.command()
    async def stop(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.clear_emote()
        stop_emote = translations.read()["translations"]["stop-emote"][get_Language]
        await ctx.send(stop_emote)               




    @client.command(aliases=['Ready'])
    async def ready(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_ready(fortnitepy.ReadyState.READY)
        ready = translations.read()["translations"]["ready"][get_Language]
        await ctx.send(ready)

    @client.command(aliases=['sitin'],)
    async def unready(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        unready = translations.read()["translations"]["unready"][get_Language]
        await ctx.send(unready)

    @client.command(
      name="level",
      aliases=[
        'niveau',
        'Level'
      ]
    )
    async def levelx(ctx: fortnitepy.ext.commands.Context, banner_level: int) -> None:
        await client.party.me.set_banner(season_level=banner_level)
        level = translations.read()["translations"]["level"][get_Language]
        await ctx.send(level.format(banner_level))





    @client.command(aliases=['ghost','Hide'])
    async def hide(ctx: fortnitepy.ext.commands.Context, *, user = None):
        await ctx.send("Error")






    @client.command()
    async def say(ctx: fortnitepy.ext.commands.Context, *, message = None):
        if message is not None:
            await client.party.send(message)
            say = translations.read()["translations"]["say"][get_Language]
            await ctx.send(say.format(message))  #message
        else:
            say_no = translations.read()["translations"]["say-no"][get_Language]
            await ctx.send(say_no)


















    return client


@Sanic.route('/dashboard', methods=['GET'])
async def root(request: sanic.request.Request) -> None:
         client_name = request.args.get('name')
         try:
          client = [c for c in clients if c.user.display_name == client_name][0]
         except IndexError:
          return sanic.response.redirect("")

         if client:

          outfit_name = await get_name(client.party.me.outfit)
          backpack_name = await get_name(client.party.me.backpack)
          pickaxe_name = await get_name(client.party.me.pickaxe)
          display_name_get = client.user.display_name 
          return sanic.response.html(
        """
<!--
=========================================================
* klldFN UI Dashboard
=========================================================
-->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="apple-touch-icon" sizes="76x76" href="https://klldfn.xyz/icon.png">
  <link rel="icon" type="image/png" href="https://klldfn.xyz/icon.png">
  <title>
    klldFN Dashboard | """ + f"""{display_name_get}""" + """
  </title>
  <!--     Fonts and icons     -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet" />
  <!-- Nucleo Icons -->
  <link href="https://klldfn-ui-dashboard.klldfn.xyz//assets/css/nucleo-icons.css" rel="stylesheet" />
  <link href="https://klldfn-ui-dashboard.klldfn.xyz//assets/css/nucleo-svg.css" rel="stylesheet" />
  <!-- Font Awesome Icons -->
  <script src="https://kit.fontawesome.com/42d5adcbca.js" crossorigin="anonymous"></script>
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-svg.css" rel="stylesheet" />
  <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
  <!-- CSS Files -->
  <link id="pagestyle" href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/klldFN-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
  <!-- Nepcha Analytics (nepcha.com) -->
  <!-- Nepcha is a easy-to-use web analytics. No cookies and fully compliant with GDPR, CCPA and PECR. -->
  <script defer data-site="YOUR_DOMAIN_HERE" src="https://api.nepcha.com/js/nepcha-analytics.js"></script>
  <style>
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(255, 255, 255, 0.8);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }

    .spinner-border {
      width: 3rem;
      height: 3rem;
    }
  </style>
</head>

<body class="g-sidenav-show  bg-gray-100">
<div class="loading-overlay" id="loadingOverlay">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <aside class="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3 bg-white" id="sidenav-main" data-color="dark">
    <div class="sidenav-header">
      <i class="fas fa-times p-3 cursor-pointer text-secondary opacity-5 position-absolute end-0 top-0 d-none d-xl-none" aria-hidden="true" id="iconSidenav"></i>
      <a class="navbar-brand m-0" href="#">
        <img src="https://klldfn.xyz/icon.png" class="navbar-brand-img h-100" alt="main_logo">
        <span class="ms-1 font-weight-bold">klldFN Dashboard</span>
      </a>
    </div>
    <hr class="horizontal dark mt-0">
    <div class="collapse navbar-collapse  w-auto " id="sidenav-collapse-main">
      <ul class="navbar-nav">
      <li class="nav-item">
          <a class="nav-link" href="/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
            <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <path class="color-background opacity-6" d="M46.7199583,10.7414583 L40.8449583,0.949791667 C40.4909749,0.360605034 39.8540131,0 39.1666667,0 L7.83333333,0 C7.1459869,0 6.50902508,0.360605034 6.15504167,0.949791667 L0.280041667,10.7414583 C0.0969176761,11.0460037 -1.23209662e-05,11.3946378 -1.23209662e-05,11.75 C-0.00758042603,16.0663731 3.48367543,19.5725301 7.80004167,19.5833333 L7.81570833,19.5833333 C9.75003686,19.5882688 11.6168794,18.8726691 13.0522917,17.5760417 C16.0171492,20.2556967 20.5292675,20.2556967 23.494125,17.5760417 C26.4604562,20.2616016 30.9794188,20.2616016 33.94575,17.5760417 C36.2421905,19.6477597 39.5441143,20.1708521 42.3684437,18.9103691 C45.1927731,17.649886 47.0084685,14.8428276 47.0000295,11.75 C47.0000295,11.3946378 46.9030823,11.0460037 46.7199583,10.7414583 Z"></path>
                        <path class="color-background" d="M39.198,22.4912623 C37.3776246,22.4928106 35.5817531,22.0149171 33.951625,21.0951667 L33.92225,21.1107282 C31.1430221,22.6838032 27.9255001,22.9318916 24.9844167,21.7998837 C24.4750389,21.605469 23.9777983,21.3722567 23.4960833,21.1018359 L23.4745417,21.1129513 C20.6961809,22.6871153 17.4786145,22.9344611 14.5386667,21.7998837 C14.029926,21.6054643 13.533337,21.3722507 13.0522917,21.1018359 C11.4250962,22.0190609 9.63246555,22.4947009 7.81570833,22.4912623 C7.16510551,22.4842162 6.51607673,22.4173045 5.875,22.2911849 L5.875,44.7220845 C5.875,45.9498589 6.7517757,46.9451667 7.83333333,46.9451667 L19.5833333,46.9451667 L19.5833333,33.6066734 L27.4166667,33.6066734 L27.4166667,46.9451667 L39.1666667,46.9451667 C40.2482243,46.9451667 41.125,45.9498589 41.125,44.7220845 L41.125,22.2822926 C40.4887822,22.4116582 39.8442868,22.4815492 39.198,22.4912623 Z"></path>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
                        </div>
            <span class="nav-link-text ms-1">Home</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link  active" href="#">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(12, 12, 12, 1);transform: ;msFilter:;"><path class="color-background"
                        d="M4 13h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1zm-1 7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v4zm10 0a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v7zm1-10h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1z">
                    </path></svg>
               </div>
            <span class="nav-link-text ms-1">Dashboard</span>
          </a>
        </li>
        <li class="nav-item">
        <a class="nav-link" href="/cosmetics?name=""" + f"""{display_name_get}""" + """"">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <i class="bx bx-user text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
            </div>
            <span class="nav-link-text ms-1">Cosmetics</span>
          </a>
          <a class="nav-link" href="https://klldfn.xyz/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <i class="ni ni-world-2 text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
            </div>
            <span class="nav-link-text ms-1">Website</span>
          </a>
        </li>
      </ul>
    </div>
    <div class="sidenav-footer mx-3 ">
      <div class="card card-background shadow-none card-background-mask-dark" id="sidenavCard">
        <div class="full-background" style="background-image: url('https://klldfn-ui-dashboard.klldfn.xyz/assets/img/curved-images/white-curved.jpg')"></div>
        <div class="card-body text-start p-3 w-100">
          <div class="icon icon-shape icon-sm bg-white shadow text-center mb-3 d-flex align-items-center justify-content-center border-radius-md">
            <i class="ni ni-diamond text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
          </div>
          <div class="docs-info">
            <h6 class="text-white up mb-0">Need help?</h6>
            <p class="text-xs font-weight-bold">Enter the Discord server</p>
            <a href="https://discord.gg/ybr7evg4q5" target="_blank" class="btn btn-white btn-sm w-100 mb-0">link</a>
          </div>
        </div>
      </div>
    </div>
  </aside>
  <main class="main-content position-relative max-height-vh-100 h-100 border-radius-lg ">
    <!-- Navbar -->
    <nav class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl position-sticky blur shadow-blur mt-4 left-auto top-1 z-index-sticky" id="navbarBlur" navbar-scroll="true">
      <div class="container-fluid py-1 px-3">
        <nav aria-label="breadcrumb">
          <h6 class="font-weight-bolder mb-0">Dashboard</h6>
        </nav>
        <div class="collapse navbar-collapse mt-sm-0 mt-2 me-md-0 me-sm-4" id="navbar">

          <div class="ms-md-auto pe-md-3 d-flex align-items-center">
            <li class="nav-item d-xl-none ps-3 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" id="iconNavbarSidenav">
                <div class="sidenav-toggler-inner">
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                </div>
              </a>

            </li>

            <li class="nav-item px-3 d-flex align-items-center">
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- End Navbar -->
    <div class="container-fluid py-4">
      <div class="row">
      <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
          <div class="card">
            <div class="card-body p-3">
              <div class="row">
                <div class="col-8">
                  <div class="numbers">
                    <p class="text-sm mb-0 text-capitalize font-weight-bold">BOT NAME</p>
                    <h5 class="font-weight-bolder mb-0">
                      """ + f""" {client.user.display_name} """ + """


                    </h5>
                  </div>
                </div>

                <div class="col-4 text-end">
                  <div class="icon icon-shape bg-gradient-primary shadow text-center border-radius-md">
                    <i class="bx bxs-bot text-lg opacity-10" aria-hidden="true"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
          <div class="card">
            <div class="card-body p-3">
              <div class="row">
                <div class="col-8">
                  <div class="numbers">
                    <p class="text-sm mb-0 text-capitalize font-weight-bold">TOTAL FRIENDS</p>
                    <h5 class="font-weight-bolder mb-0">
                      """ + f""" {len(client.friends)} """ + """
                     <!-- <span class="text-success text-sm font-weight-bolder"></span> -->
                    </h5>
                  </div>
                </div>
                <div class="col-4 text-end">
                  <div class="icon icon-shape bg-gradient-primary shadow text-center border-radius-md">
                  <i class="ni ni-single-02 text-lg opacity-10" aria-hidden="true"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
          <div class="card">
            <div class="card-body p-3">
              <div class="row">
                <div class="col-8">
                  <div class="numbers">
                    <p class="text-sm mb-0 text-capitalize font-weight-bold">PIATFORM</p>
                    <h5 class="font-weight-bolder mb-0">
                      """ + f""" {(str((client.platform))[9:]).lower().capitalize()} """ + """


                    </h5>
                  </div>
                </div>

                <div class="col-4 text-end">
                  <div class="icon icon-shape bg-gradient-primary shadow text-center border-radius-md">
                    <i class="ni ni-tv-2 text-lg opacity-10" aria-hidden="true"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      <div class="row mt-4">
        <div class="col-lg-7 mb-lg-0 mb-4">
          <div class="card">
            <div class="card-body p-3">
              <div class="row">
                <div class="col-lg-6">
                  <div class="d-flex flex-column h-100">
                    <h5 class="font-weight-bolder">klldFN 2.0.0b1</h5>
                    <p class="mb-5">Available now with enhancements and fixes</p>
                    <!--
                    <a class="text-body text-sm font-weight-bold mb-0 icon-move-right mt-auto" href="javascript:;">
                      Read More
                      <i class="fas fa-arrow-right text-sm ms-1" aria-hidden="true"></i>
                    </a>
                  -->
                  </div>
                </div>
                <div class="col-lg-5 ms-auto text-center mt-5 mt-lg-0">
                  <div class="bg-gradient-primary border-radius-lg h-100">
                    <img src="https://klldfn-ui-dashboard.klldfn.xyz//assets/img/shapes/waves-white.svg" class="position-absolute h-100 w-50 top-0 d-lg-block d-none" alt="waves">
                    <div class="position-relative d-flex align-items-center justify-content-center h-100">
                      <img class="w-100 position-relative z-index-2 pt-4" src="https://klldfn-ui-dashboard.klldfn.xyz//assets/img/illustrations/rocket-white.png" alt="rocket">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-5">
          <div class="card h-100 p-3">
            <div class="overflow-hidden position-relative border-radius-lg bg-cover h-100" style="background-image: url('https://klldfn-ui-dashboard.klldfn.xyz//assets/img/snapedit_1712834729188.png');">
              <span class="mask bg-gradient-dark"></span>
              <div class="card-body position-relative z-index-1 d-flex flex-column h-100 p-3">
                <h5 class="text-white font-weight-bolder mb-4 pt-2">Party Size</h5>
                <p class="text-white">""" + f"""{str(client.party.member_count)}""" + """/16</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 mt-4">
        <div class="card mb-4">
          <div class="card-header pb-0 p-3">
            <h6 class="mb-1">Locker</h6>
          </div>
          <div class="card-body p-3">
            <div class="row">
              <div class="col-xl-3 col-md-6 mb-xl-0 mb-4">
                <div class="card card-blog card-plain">
                  <div class="position-relative">
                    <a class="d-block shadow-xl border-radius-xl">
                      <img src="https://fortnite-api.com/images/cosmetics/br/""" + f"""{client.party.me.outfit}""" + """/icon.png" alt="img-blur-shadow" class="w-100 border-radius-lg shadow-sm">
                    </a>
                  </div>
                  <div class="card-body px-1 pb-0">
                    <a href="javascript:;">
                      <h5>
                        Outfit
                      </h5>
                    </a>
                    <p class="mb-4 text-sm">
                     """ + f""" {outfit_name} """ + """
                    </p>
                    <div class="d-flex align-items-center justify-content-between">
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-xl-3 col-md-6 mb-xl-0 mb-4">
                <div class="card card-blog card-plain">
                  <div class="position-relative">
                    <a class="d-block shadow-xl border-radius-xl">
                      <img src="https://fortnite-api.com/images/cosmetics/br/""" + f"""{client.party.me.backpack}""" + """/icon.png" alt="img-blur-shadow" class="w-100 border-radius-lg shadow-sm">
                    </a>
                  </div>
                  <div class="card-body px-1 pb-0">
                    <a href="javascript:;">
                      <h5>
                        Backpack
                      </h5>
                    </a>
                    <p class="mb-4 text-sm">
                      """ + f""" {backpack_name} """ + """
                    </p>
                    <div class="d-flex align-items-center justify-content-between">
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-xl-3 col-md-6 mb-xl-0 mb-4">
                <div class="card card-blog card-plain">
                  <div class="position-relative">
                    <a class="d-block shadow-xl border-radius-xl">
                      <img src="https://fortnite-api.com/images/cosmetics/br/""" + f"""{client.party.me.pickaxe}""" + """/icon.png" alt="img-blur-shadow" class="w-100 border-radius-lg shadow-sm">
                    </a>
                  </div>
                  <div class="card-body px-1 pb-0">
                    <a href="javascript:;">
                      <h5>
                        Pickaxe
                      </h5>
                    </a>
                    <p class="mb-4 text-sm">
                      """ + f""" {pickaxe_name} """ + """
                    </p>
                    <div class="d-flex align-items-center justify-content-between">
                    </div>
                  </div>
                </div>
              </div>  

          </div>
        </div>
      </div>
    </div>

      <footer class="footer py-5">
      <div class="container">
        <div class="row">
        </div>
        <div class="row">
          <div class="col-8 mx-auto text-center mt-1">
            <p class="mb-0 text-secondary">
              Copyright © <script>
                document.write(new Date().getFullYear())
              </script>,
              <i class="fa fa-heart"></i> by
              klldFN
              All Right Reserved
            </p>
          </div>
        </div>
      </div>
    </footer>
    </div>
  </main>

  <!--   Core JS Files   -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/popper.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/bootstrap.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/perfect-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/smooth-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/chartjs.min.js"></script>
  <script>
    var ctx = document.getElementById("chart-bars").getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Sales",
          tension: 0.4,
          borderWidth: 0,
          borderRadius: 4,
          borderSkipped: false,
          backgroundColor: "#fff",
          data: [450, 200, 100, 220, 500, 100, 400, 230, 500],
          maxBarThickness: 6
        }, ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
            },
            ticks: {
              suggestedMin: 0,
              suggestedMax: 500,
              beginAtZero: true,
              padding: 15,
              font: {
                size: 14,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
              color: "#fff"
            },
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false
            },
            ticks: {
              display: false
            },
          },
        },
      },
    });


    var ctx2 = document.getElementById("chart-line").getContext("2d");

    var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke1.addColorStop(1, 'rgba(203,12,159,0.2)');
    gradientStroke1.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke1.addColorStop(0, 'rgba(203,12,159,0)'); //purple colors

    var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke2.addColorStop(1, 'rgba(20,23,39,0.2)');
    gradientStroke2.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke2.addColorStop(0, 'rgba(20,23,39,0)'); //purple colors

    new Chart(ctx2, {
      type: "line",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
            label: "Mobile apps",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#cb0c9f",
            borderWidth: 3,
            backgroundColor: gradientStroke1,
            fill: true,
            data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
            maxBarThickness: 6

          },
          {
            label: "Websites",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#3A416F",
            borderWidth: 3,
            backgroundColor: gradientStroke2,
            fill: true,
            data: [30, 90, 40, 140, 290, 290, 340, 230, 400],
            maxBarThickness: 6
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              padding: 10,
              color: '#b2b9bf',
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              color: '#b2b9bf',
              padding: 20,
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });
  </script>
  <script>
    var win = navigator.platform.indexOf('Win') > -1;
    if (win && document.querySelector('#sidenav-scrollbar')) {
      var options = {
        damping: '0.5'
      }
      Scrollbar.init(document.querySelector('#sidenav-scrollbar'), options);
    }
  </script>
  <script>
    // Simulate content loaded event
    window.addEventListener('load', function() {
      // Hide loading overlay after 3 seconds (adjust the duration as needed)
      setTimeout(function() {
        document.getElementById('loadingOverlay').style.display = 'none';
      }, 3000); // Duration in milliseconds (e.g., 3000 for 3 seconds)
    });
  </script>
  <!-- Github buttons -->
  <script async defer src="https://buttons.github.io/buttons.js"></script>
  <!-- Control Center for Soft Dashboard: parallax effects, scripts for the example pages etc -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/soft-ui-dashboard.min.js?v=1.0.7"></script>
</body>

</html>
        """
    )

template_html_ss = """
<!--
=========================================================
* klldFN UI Dashboard
=========================================================
-->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="apple-touch-icon" sizes="76x76" href="https://klldfn.xyz/icon.png">
  <link rel="icon" type="image/png" href="https://klldfn.xyz/icon.png">
  <title>
    klldFN Dashboard
  </title>
  <!--     Fonts and icons     -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet" />
  <!-- Nucleo Icons -->
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-icons.css" rel="stylesheet" />
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-svg.css" rel="stylesheet" />
  <!-- Font Awesome Icons -->
  <script src="https://kit.fontawesome.com/42d5adcbca.js" crossorigin="anonymous"></script>
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-svg.css" rel="stylesheet" />
  <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
  <!-- CSS Files -->
  <link id="pagestyle" href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/klldFN-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
  <!-- Nepcha Analytics (nepcha.com) -->
  <!-- Nepcha is a easy-to-use web analytics. No cookies and fully compliant with GDPR, CCPA and PECR. -->
  <script defer data-site="klldFN.xyz" src="https://api.nepcha.com/js/nepcha-analytics.js"></script>
  <style>
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(255, 255, 255, 0.8);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }

    .spinner-border {
      width: 3rem;
      height: 3rem;
    }
  </style>
</head>

<body class="g-sidenav-show  bg-gray-100">
  <div class="loading-overlay" id="loadingOverlay">
    <div class="spinner-border" role="status">

    </div>
  </div>

  <aside class="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3 bg-white" id="sidenav-main" data-color="dark">
    <div class="sidenav-header">
      <i class="fas fa-times p-3 cursor-pointer text-secondary opacity-5 position-absolute end-0 top-0 d-none d-xl-none" aria-hidden="true" id="iconSidenav"></i>
      <a class="navbar-brand m-0" href="#">
        <img src="https://klldfn.xyz/icon.png" class="navbar-brand-img h-100" alt="main_logo">
        <span class="ms-1 font-weight-bold">klldFN Dashboard</span>
      </a>
    </div>
    <hr class="horizontal dark mt-0">
    <div class="collapse navbar-collapse  w-auto " id="sidenav-collapse-main">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" href="/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
            <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <path class="color-background opacity-6" d="M46.7199583,10.7414583 L40.8449583,0.949791667 C40.4909749,0.360605034 39.8540131,0 39.1666667,0 L7.83333333,0 C7.1459869,0 6.50902508,0.360605034 6.15504167,0.949791667 L0.280041667,10.7414583 C0.0969176761,11.0460037 -1.23209662e-05,11.3946378 -1.23209662e-05,11.75 C-0.00758042603,16.0663731 3.48367543,19.5725301 7.80004167,19.5833333 L7.81570833,19.5833333 C9.75003686,19.5882688 11.6168794,18.8726691 13.0522917,17.5760417 C16.0171492,20.2556967 20.5292675,20.2556967 23.494125,17.5760417 C26.4604562,20.2616016 30.9794188,20.2616016 33.94575,17.5760417 C36.2421905,19.6477597 39.5441143,20.1708521 42.3684437,18.9103691 C45.1927731,17.649886 47.0084685,14.8428276 47.0000295,11.75 C47.0000295,11.3946378 46.9030823,11.0460037 46.7199583,10.7414583 Z"></path>
                        <path class="color-background" d="M39.198,22.4912623 C37.3776246,22.4928106 35.5817531,22.0149171 33.951625,21.0951667 L33.92225,21.1107282 C31.1430221,22.6838032 27.9255001,22.9318916 24.9844167,21.7998837 C24.4750389,21.605469 23.9777983,21.3722567 23.4960833,21.1018359 L23.4745417,21.1129513 C20.6961809,22.6871153 17.4786145,22.9344611 14.5386667,21.7998837 C14.029926,21.6054643 13.533337,21.3722507 13.0522917,21.1018359 C11.4250962,22.0190609 9.63246555,22.4947009 7.81570833,22.4912623 C7.16510551,22.4842162 6.51607673,22.4173045 5.875,22.2911849 L5.875,44.7220845 C5.875,45.9498589 6.7517757,46.9451667 7.83333333,46.9451667 L19.5833333,46.9451667 L19.5833333,33.6066734 L27.4166667,33.6066734 L27.4166667,46.9451667 L39.1666667,46.9451667 C40.2482243,46.9451667 41.125,45.9498589 41.125,44.7220845 L41.125,22.2822926 C40.4887822,22.4116582 39.8442868,22.4815492 39.198,22.4912623 Z"></path>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
                        </div>
            <span class="nav-link-text ms-1">Home</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="https://klldfn.xyz/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <i class="ni ni-world-2 text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
            </div>
            <span class="nav-link-text ms-1">Website</span>
          </a>
        </li>

      </ul>
    </div>
    <div class="sidenav-footer mx-3 ">
      <div class="card card-background shadow-none card-background-mask-dark" id="sidenavCard">
        <div class="full-background" style="background-image: url('https://klldfn-ui-dashboard.klldfn.xyz/assets/img/curved-images/white-curved.jpg')"></div>
        <div class="card-body text-start p-3 w-100">
          <div class="icon icon-shape icon-sm bg-white shadow text-center mb-3 d-flex align-items-center justify-content-center border-radius-md">
            <i class="ni ni-diamond text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
          </div>
          <div class="docs-info">
            <h6 class="text-white up mb-0">Need help?</h6>
            <p class="text-xs font-weight-bold">Enter the Discord server</p>
            <a href="https://discord.gg/ybr7evg4q5" target="_blank" class="btn btn-white btn-sm w-100 mb-0">link</a>
          </div>
        </div>
      </div>
    </div>

  </aside>
  <main class="main-content position-relative max-height-vh-100 h-100 border-radius-lg ">
    <!-- Navbar -->
    <nav class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl position-sticky blur shadow-blur mt-4 left-auto top-1 z-index-sticky" id="navbarBlur" navbar-scroll="true">
      <div class="container-fluid py-1 px-3">
        <nav aria-label="breadcrumb">
          <h6 class="font-weight-bolder mb-0">Dashboard</h6>
        </nav>
        <div class="collapse navbar-collapse mt-sm-0 mt-2 me-md-0 me-sm-4" id="navbar">

          <div class="ms-md-auto pe-md-3 d-flex align-items-center">
            <!--
            <div class="input-group">
              <span class="input-group-text text-body"><i class="fas fa-search" aria-hidden="true"></i></span>
              <input type="text" class="form-control" placeholder="Type here...">
            </div>
          </div>
          <ul class="navbar-nav  justify-content-end">

            <li class="nav-item d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body font-weight-bold px-0">
                <i class="fa fa-user me-sm-1"></i>
                <span class="d-sm-inline d-none">Sign In</span>
              </a>
            </li>
              -->
            <li class="nav-item d-xl-none ps-3 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" id="iconNavbarSidenav">
                <div class="sidenav-toggler-inner">
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                </div>
              </a>

            </li>

            <li class="nav-item px-3 d-flex align-items-center">
            </li>
            <!--
            <li class="nav-item dropdown pe-2 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fa fa-bell cursor-pointer"></i>
              </a>
              <ul class="dropdown-menu  dropdown-menu-end  px-2 py-3 me-sm-n4" aria-labelledby="dropdownMenuButton">
                <h6 class="text-sm font-weight-normal mb-1">
                  No New notifications
                </h6>
              </ul>
            </li>
            -->
          </ul>
        </div>
      </div>
    </nav>
    <!-- End Navbar -->
    <main class="main-content  mt-0">
      <div class="col-12 mt-4">
        <div class="card mb-4">
          <div class="card-header pb-0 p-3">
            <h6 class="mb-1">Lobbybot</h6>
          </div>
          <div class="card-body p-3">
            <div class="row">
            {% if clients %}
              {% for client in clients %} 
              <div class="col-xl-3 col-md-6 mb-xl-0 mb-4">
                <div class="card card-blog card-plain">
                  <div class="position-relative">
                    <a class="d-block shadow-xl border-radius-xl">
                      <img src="https://fortnite-api.com/images/cosmetics/br/{{ client.outfit }}/icon.png" alt="img-blur-shadow" class="w-100 border-radius-lg shadow-sm">
                    </a>
                  </div>
                  <div class="card-body px-1 pb-0">
                    <a href="dashboard?name={{client.display_name}}">
                      <h5>
                        {{ client.display_name }}
                      </h5>
                    </a>
                    <p class="mb-4 text-sm">
                      Friends: {{ client.friends_count }}
                    </p>
                    <div class="d-flex align-items-center justify-content-between">
                    </div>
                  </div>
                </div>
              </div>

              {% endfor %}
              {% else %}
              <p class="">Client Information Not Available</p>
              {% endif %}
          </div>
        </div>
      </div>
    </div>
    </main>


    <footer class="footer py-5">
      <div class="container">
        <div class="row">
        </div>
        <div class="row">
          <div class="col-8 mx-auto text-center mt-1">
            <p class="mb-0 text-secondary">
              Copyright © <script>
                document.write(new Date().getFullYear())
              </script>,
              <i class="fa fa-heart"></i> by
              klldFN
              All Right Reserved
            </p>
          </div>
        </div>
      </div>
    </footer>


  <!--   Core JS Files   -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/popper.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/bootstrap.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/perfect-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/smooth-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/chartjs.min.js"></script>


  <script>
    var ctx = document.getElementById("chart-bars").getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Sales",
          tension: 0.4,
          borderWidth: 0,
          borderRadius: 4,
          borderSkipped: false,
          backgroundColor: "#fff",
          data: [450, 200, 100, 220, 500, 100, 400, 230, 500],
          maxBarThickness: 6
        }, ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
            },
            ticks: {
              suggestedMin: 0,
              suggestedMax: 500,
              beginAtZero: true,
              padding: 15,
              font: {
                size: 14,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
              color: "#fff"
            },
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false
            },
            ticks: {
              display: false
            },
          },
        },
      },
    });


    var ctx2 = document.getElementById("chart-line").getContext("2d");

    var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke1.addColorStop(1, 'rgba(203,12,159,0.2)');
    gradientStroke1.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke1.addColorStop(0, 'rgba(203,12,159,0)'); //purple colors

    var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke2.addColorStop(1, 'rgba(20,23,39,0.2)');
    gradientStroke2.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke2.addColorStop(0, 'rgba(20,23,39,0)'); //purple colors

    new Chart(ctx2, {
      type: "line",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
            label: "Mobile apps",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#cb0c9f",
            borderWidth: 3,
            backgroundColor: gradientStroke1,
            fill: true,
            data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
            maxBarThickness: 6

          },
          {
            label: "Websites",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#3A416F",
            borderWidth: 3,
            backgroundColor: gradientStroke2,
            fill: true,
            data: [30, 90, 40, 140, 290, 290, 340, 230, 400],
            maxBarThickness: 6
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              padding: 10,
              color: '#b2b9bf',
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              color: '#b2b9bf',
              padding: 20,
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });
  </script>
  <script>
    var win = navigator.platform.indexOf('Win') > -1;
    if (win && document.querySelector('#sidenav-scrollbar')) {
      var options = {
        damping: '0.5'
      }
      Scrollbar.init(document.querySelector('#sidenav-scrollbar'), options);
    }
  </script>
  <script>
    // Simulate content loaded event
    window.addEventListener('load', function() {
      // Hide loading overlay after 3 seconds (adjust the duration as needed)
      setTimeout(function() {
        document.getElementById('loadingOverlay').style.display = 'none';
      }, 3000); // Duration in milliseconds (e.g., 3000 for 3 seconds)
    });
  </script>
  <!-- Github buttons -->
  <script async defer src="https://buttons.github.io/buttons.js"></script>
  <!-- Control Center for Soft Dashboard: parallax effects, scripts for the example pages etc -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz//assets/js/soft-ui-dashboard.min.js?v=1.0.7"></script>
</body>

</html>
"""

@Sanic.route('/', methods=['GET', 'POST'])
async def client_info(request):
      template = Template(template_html_ss)
      if request.method == 'GET':
        # Pass the clients list to the template context
        client_info = []
        for client in clients:
            client_info.append({
                'display_name': client.user.display_name,
                'outfit': client.party.me.outfit,
                'friends_count': len(client.friends)
                # Add more client information here as needed
            })

        # Render the template with client information
        return sanic.response.html(template.render(clients=client_info))


@Sanic.route('/cosmetics', methods=['GET'])
async def cosmetics_route(request: Request):
        client_name = request.args.get('name')
        try:
          client = [c for c in clients if c.user.display_name == client_name][0]
        except IndexError:
          return sanic.response.html("Client not found")

        if client:
          if request.method == 'GET':
            display_name_get = client.user.display_name
            return sanic.response.html("""
<!--
=========================================================
* klldFN UI Dashboard
=========================================================
-->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="apple-touch-icon" sizes="76x76" href="https://klldfn.xyz/icon.png">
  <link rel="icon" type="image/png" href="https://klldfn.xyz/icon.png">
  <title>
    klldFN Dashboard | Cosmetics
  </title>
  <!--     Fonts and icons     -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet" />
  <!-- Nucleo Icons -->
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-icons.css" rel="stylesheet" />
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-svg.css" rel="stylesheet" />
  <!-- Font Awesome Icons -->
  <script src="https://kit.fontawesome.com/42d5adcbca.js" crossorigin="anonymous"></script>
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-svg.css" rel="stylesheet" />
  <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
  <!-- CSS Files -->
  <link id="pagestyle" href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/klldFN-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
  <!-- Nepcha Analytics (nepcha.com) -->
  <!-- Nepcha is a easy-to-use web analytics. No cookies and fully compliant with GDPR, CCPA and PECR. -->

  <script defer data-site="YOUR_DOMAIN_HERE" src="https://api.nepcha.com/js/nepcha-analytics.js"></script>
  <style>
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(255, 255, 255, 0.8);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }

    .spinner-border {
      width: 3rem;
      height: 3rem;
    }
  </style>

</head>

<body class="g-sidenav-show  bg-gray-100">
  <div class="loading-overlay" id="loadingOverlay">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <aside class="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3 bg-white" id="sidenav-main" data-color="dark">
    <div class="sidenav-header">
      <i class="fas fa-times p-3 cursor-pointer text-secondary opacity-5 position-absolute end-0 top-0 d-none d-xl-none" aria-hidden="true" id="iconSidenav"></i>
      <a class="navbar-brand m-0" href="#">
        <img src="https://klldfn.xyz/icon.png" class="navbar-brand-img h-100" alt="main_logo">
        <span class="ms-1 font-weight-bold">klldFN Dashboard</span>
      </a>
    </div>
    <hr class="horizontal dark mt-0">
    <div class="collapse navbar-collapse  w-auto " id="sidenav-collapse-main">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
            <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <path class="color-background opacity-6" d="M46.7199583,10.7414583 L40.8449583,0.949791667 C40.4909749,0.360605034 39.8540131,0 39.1666667,0 L7.83333333,0 C7.1459869,0 6.50902508,0.360605034 6.15504167,0.949791667 L0.280041667,10.7414583 C0.0969176761,11.0460037 -1.23209662e-05,11.3946378 -1.23209662e-05,11.75 C-0.00758042603,16.0663731 3.48367543,19.5725301 7.80004167,19.5833333 L7.81570833,19.5833333 C9.75003686,19.5882688 11.6168794,18.8726691 13.0522917,17.5760417 C16.0171492,20.2556967 20.5292675,20.2556967 23.494125,17.5760417 C26.4604562,20.2616016 30.9794188,20.2616016 33.94575,17.5760417 C36.2421905,19.6477597 39.5441143,20.1708521 42.3684437,18.9103691 C45.1927731,17.649886 47.0084685,14.8428276 47.0000295,11.75 C47.0000295,11.3946378 46.9030823,11.0460037 46.7199583,10.7414583 Z"></path>
                        <path class="color-background" d="M39.198,22.4912623 C37.3776246,22.4928106 35.5817531,22.0149171 33.951625,21.0951667 L33.92225,21.1107282 C31.1430221,22.6838032 27.9255001,22.9318916 24.9844167,21.7998837 C24.4750389,21.605469 23.9777983,21.3722567 23.4960833,21.1018359 L23.4745417,21.1129513 C20.6961809,22.6871153 17.4786145,22.9344611 14.5386667,21.7998837 C14.029926,21.6054643 13.533337,21.3722507 13.0522917,21.1018359 C11.4250962,22.0190609 9.63246555,22.4947009 7.81570833,22.4912623 C7.16510551,22.4842162 6.51607673,22.4173045 5.875,22.2911849 L5.875,44.7220845 C5.875,45.9498589 6.7517757,46.9451667 7.83333333,46.9451667 L19.5833333,46.9451667 L19.5833333,33.6066734 L27.4166667,33.6066734 L27.4166667,46.9451667 L39.1666667,46.9451667 C40.2482243,46.9451667 41.125,45.9498589 41.125,44.7220845 L41.125,22.2822926 C40.4887822,22.4116582 39.8442868,22.4815492 39.198,22.4912623 Z"></path>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
                        </div>
            <span class="nav-link-text ms-1">Home</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/dashboard?name=""" + f"""{display_name_get}""" + """"">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="15px" height="15px" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);transform: ;msFilter:;"><path d="M4 13h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1zm-1 7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v4zm10 0a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v7zm1-10h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1z"></path></svg>  
            </div>
            <span class="nav-link-text ms-1">Dashboard</span>
          </a>
        </li>

        <li class="nav-item">
        <a class="nav-link active" href="/cosmetics?name=""" + f"""{display_name_get}""" + """">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="15px" height="15px" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(12, 12, 12, 1);transform: ;msFilter:;"><path class="color-background" d="M12 2a5 5 0 1 0 5 5 5 5 0 0 0-5-5zm0 8a3 3 0 1 1 3-3 3 3 0 0 1-3 3zm9 11v-1a7 7 0 0 0-7-7h-4a7 7 0 0 0-7 7v1h2v-1a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v1z"></path></svg>
          </div>
            <span class="nav-link-text ms-1">Cosmetics</span>
          </a>
          </li> 
          <li class="nav-item">
          <a class="nav-link" href="https://klldfn.xyz/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <i class="ni ni-world-2 text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
            </div>
            <span class="nav-link-text ms-1">Website</span>
          </a>

        </li>
      </ul>
    </div>
    <div class="sidenav-footer mx-3 ">
      <div class="card card-background shadow-none card-background-mask-dark" id="sidenavCard">
        <div class="full-background" style="background-image: url('https://klldfn-ui-dashboard.klldfn.xyz/assets/img/curved-images/white-curved.jpg')"></div>
        <div class="card-body text-start p-3 w-100">
          <div class="icon icon-shape icon-sm bg-white shadow text-center mb-3 d-flex align-items-center justify-content-center border-radius-md">
            <i class="ni ni-diamond text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
          </div>
          <div class="docs-info">
            <h6 class="text-white up mb-0">Need help?</h6>
            <p class="text-xs font-weight-bold">Enter the Discord server</p>
            <a href="https://discord.gg/ybr7evg4q5" target="_blank" class="btn btn-white btn-sm w-100 mb-0">link</a>
          </div>
        </div>
      </div>
    </div>

  </aside>
  <main class="main-content position-relative max-height-vh-100 h-100 border-radius-lg ">
    <!-- Navbar -->
    <nav class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl position-sticky blur shadow-blur mt-4 left-auto top-1 z-index-sticky" id="navbarBlur" navbar-scroll="true">
      <div class="container-fluid py-1 px-3">
        <nav aria-label="breadcrumb">
          <h6 class="font-weight-bolder mb-0">Dashboard</h6>
        </nav>
        <div class="collapse navbar-collapse mt-sm-0 mt-2 me-md-0 me-sm-4" id="navbar">

          <div class="ms-md-auto pe-md-3 d-flex align-items-center">
            <!--
            <div class="input-group">
              <span class="input-group-text text-body"><i class="fas fa-search" aria-hidden="true"></i></span>
              <input type="text" class="form-control" placeholder="Type here...">
            </div>
          </div>
          <ul class="navbar-nav  justify-content-end">

            <li class="nav-item d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body font-weight-bold px-0">
                <i class="fa fa-user me-sm-1"></i>
                <span class="d-sm-inline d-none">Sign In</span>
              </a>
            </li>
              -->
            <li class="nav-item d-xl-none ps-3 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" id="iconNavbarSidenav">
                <div class="sidenav-toggler-inner">
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                </div>
              </a>

            </li>

            <li class="nav-item px-3 d-flex align-items-center">
            </li>
            <!--
            <li class="nav-item dropdown pe-2 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fa fa-bell cursor-pointer"></i>
              </a>
              <ul class="dropdown-menu  dropdown-menu-end  px-2 py-3 me-sm-n4" aria-labelledby="dropdownMenuButton">
                <h6 class="text-sm font-weight-normal mb-1">
                  No New notifications
                </h6>
              </ul>
            </li>
            -->
          </ul>
        </div>
      </div>
    </nav>
    <!-- End Navbar -->
    <main class="main-content mt-0">
        <section>
            <div class="page-header min-vh-75">
                <div class="container" style="display: grid; grid-template-columns: repeat(2, 3fr); gap: 20px;">
                    <div class="row">
                        <div class="col-xl-4 col-lg-5 col-md-6 d-flex flex-column mx-auto">
                            <div class="card card-plain mt-8">
                                <div class="card-body">
                                    <div class="container" style="display: grid; grid-template-columns: repeat(2, 3fr); gap: 20px;">
                                        <div class="box" style="position: relative; width: 250px; height: 250px; border: 1px solid #dbd1d1; overflow: hidden; background-color: #cac1c1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; text-align: center;">
                                            <a href="cosmetics/skin?name=""" + f"""{display_name_get}""" + """" style="display: block; text-decoration: none; color: inherit;">
                                                <img src="https://static.wikia.nocookie.net/fortnite/images/7/7a/Outfit_-_Icon_-_Fortnite.png" alt="Image 1" style="width: 100%; height: auto; display: block;">
                                                <p style="margin: 0; font-size: 16px; color: #333;">Skin</p>
                                            </a>
                                        </div>
                                        <div class="box" style="position: relative; width: 250px; height: 250px; border: 1px solid #dbd1d1; overflow: hidden; background-color: #cac1c1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; text-align: center;">
                                            <a href="cosmetics/emote?name=""" + f"""{display_name_get}""" + """" style="display: block; text-decoration: none; color: inherit;">
                                                <img src="https://static.wikia.nocookie.net/fortnite/images/b/b1/Emotes_-_Icon_-_Fortnite.png" alt="Image 2" style="width: 100%; height: auto; display: block;">
                                                <p style="margin: 0; font-size: 16px; color: #333;">Emote</p>
                                            </a>
                                        </div>
                                        <div class="box" style="position: relative; width: 250px; height: 250px; border: 1px solid #dbd1d1; overflow: hidden; background-color: #cac1c1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; text-align: center;">
                                            <a href="#" data-bs-toggle="modal" data-bs-target="#CosmeticsModal" style="display: block; text-decoration: none; color: inherit;">
                                                <img src="https://static.wikia.nocookie.net/fortnite/images/1/1b/Back_Bling_-_Icon_-_Fortnite.png" alt="Image 3" style="width: 100%; height: auto; display: block;">
                                                <p style="margin: 0; font-size: 16px; color: #333;">Backpack</p>
                                            </a>
                                        </div>
                                        <div class="box" style="position: relative; width: 250px; height: 250px; border: 1px solid #dbd1d1; overflow: hidden; background-color: #cac1c1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; text-align: center;">
                                            <a href="#" data-bs-toggle="modal" data-bs-target="#CosmeticsModal" style="display: block; text-decoration: none; color: inherit;">
                                                <img src="https://static.wikia.nocookie.net/fortnite/images/f/f9/Harvesting_Tool_-_Icon_-_Fortnite.png" alt="Image 4" style="width: 100%; height: auto; display: block;">
                                                <p style="margin: 0; font-size: 16px; color: #333;">Pickaxe</p>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Modal -->
    <div class="modal fade" id="CosmeticsModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">

          </div>
          <div class="modal-body">
            This option does not work
          </div>
          <div class="modal-footer">

          </div>
        </div>
      </div>
    </div>
    <footer class="footer py-5">
      <div class="container">
        <div class="row">
        </div>
        <div class="row">
          <div class="col-8 mx-auto text-center mt-1">
            <p class="mb-0 text-secondary">
              Copyright © <script>
                document.write(new Date().getFullYear())
              </script>,
              <i class="fa fa-heart"></i> by
              klldFN
              All Right Reserved
            </p>
          </div>
        </div>
      </div>
    </footer>


  <!--   Core JS Files   -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/popper.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/bootstrap.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/perfect-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/smooth-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/chartjs.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>


  <script>
    var ctx = document.getElementById("chart-bars").getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Sales",
          tension: 0.4,
          borderWidth: 0,
          borderRadius: 4,
          borderSkipped: false,
          backgroundColor: "#fff",
          data: [450, 200, 100, 220, 500, 100, 400, 230, 500],
          maxBarThickness: 6
        }, ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
            },
            ticks: {
              suggestedMin: 0,
              suggestedMax: 500,
              beginAtZero: true,
              padding: 15,
              font: {
                size: 14,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
              color: "#fff"
            },
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false
            },
            ticks: {
              display: false
            },
          },
        },
      },
    });


    var ctx2 = document.getElementById("chart-line").getContext("2d");

    var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke1.addColorStop(1, 'rgba(203,12,159,0.2)');
    gradientStroke1.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke1.addColorStop(0, 'rgba(203,12,159,0)'); //purple colors

    var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke2.addColorStop(1, 'rgba(20,23,39,0.2)');
    gradientStroke2.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke2.addColorStop(0, 'rgba(20,23,39,0)'); //purple colors

    new Chart(ctx2, {
      type: "line",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
            label: "Mobile apps",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#cb0c9f",
            borderWidth: 3,
            backgroundColor: gradientStroke1,
            fill: true,
            data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
            maxBarThickness: 6

          },
          {
            label: "Websites",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#3A416F",
            borderWidth: 3,
            backgroundColor: gradientStroke2,
            fill: true,
            data: [30, 90, 40, 140, 290, 290, 340, 230, 400],
            maxBarThickness: 6
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              padding: 10,
              color: '#b2b9bf',
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              color: '#b2b9bf',
              padding: 20,
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });
  </script>
  <script>
    var win = navigator.platform.indexOf('Win') > -1;
    if (win && document.querySelector('#sidenav-scrollbar')) {
      var options = {
        damping: '0.5'
      }
      Scrollbar.init(document.querySelector('#sidenav-scrollbar'), options);
    }
  </script>
  <script>
    // Simulate content loaded event
    window.addEventListener('load', function() {
      // Hide loading overlay after 3 seconds (adjust the duration as needed)
      setTimeout(function() {
        document.getElementById('loadingOverlay').style.display = 'none';
      }, 3000); // Duration in milliseconds (e.g., 3000 for 3 seconds)
    });
  </script>
  <!-- Github buttons -->
  <script async defer src="https://buttons.github.io/buttons.js"></script>
  <!-- Control Center for Soft Dashboard: parallax effects, scripts for the example pages etc -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/soft-ui-dashboard.min.js?v=1.0.7"></script>
</body>

</html>
""")


template_html = """
<!--
=========================================================
* klldFN UI Dashboard
=========================================================
-->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="apple-touch-icon" sizes="76x76" href="https://klldfn.xyz/icon.png">
  <link rel="icon" type="image/png" href="https://klldfn.xyz/icon.png">
  <title>
    klldFN Dashboard | Cosmetics
  </title>
  <!--     Fonts and icons     -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet" />
  <!-- Nucleo Icons -->
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-icons.css" rel="stylesheet" />
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-svg.css" rel="stylesheet" />
  <!-- Font Awesome Icons -->
  <script src="https://kit.fontawesome.com/42d5adcbca.js" crossorigin="anonymous"></script>
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-svg.css" rel="stylesheet" />
  <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
  <!-- CSS Files -->
  <link id="pagestyle" href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/klldFN-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
  <!-- Nepcha Analytics (nepcha.com) -->
  <!-- Nepcha is a easy-to-use web analytics. No cookies and fully compliant with GDPR, CCPA and PECR. -->
  <script defer data-site="klldFN.xyz" src="https://api.nepcha.com/js/nepcha-analytics.js"></script>
  <style>
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(255, 255, 255, 0.8);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }

    .spinner-border {
      width: 3rem;
      height: 3rem;
    }
  </style>
</head>

<body class="g-sidenav-show  bg-gray-100">
  <div class="loading-overlay" id="loadingOverlay">
    <div class="spinner-border" role="status">

    </div>
  </div>

  <aside class="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3 bg-white" id="sidenav-main" data-color="dark">
    <div class="sidenav-header">
      <i class="fas fa-times p-3 cursor-pointer text-secondary opacity-5 position-absolute end-0 top-0 d-none d-xl-none" aria-hidden="true" id="iconSidenav"></i>
      <a class="navbar-brand m-0" href="#">
        <img src="https://klldfn.xyz/icon.png" class="navbar-brand-img h-100" alt="main_logo">
        <span class="ms-1 font-weight-bold">klldFN Dashboard</span>
      </a>
    </div>
    <hr class="horizontal dark mt-0">
    <div class="collapse navbar-collapse  w-auto " id="sidenav-collapse-main">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
            <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <path class="color-background opacity-6" d="M46.7199583,10.7414583 L40.8449583,0.949791667 C40.4909749,0.360605034 39.8540131,0 39.1666667,0 L7.83333333,0 C7.1459869,0 6.50902508,0.360605034 6.15504167,0.949791667 L0.280041667,10.7414583 C0.0969176761,11.0460037 -1.23209662e-05,11.3946378 -1.23209662e-05,11.75 C-0.00758042603,16.0663731 3.48367543,19.5725301 7.80004167,19.5833333 L7.81570833,19.5833333 C9.75003686,19.5882688 11.6168794,18.8726691 13.0522917,17.5760417 C16.0171492,20.2556967 20.5292675,20.2556967 23.494125,17.5760417 C26.4604562,20.2616016 30.9794188,20.2616016 33.94575,17.5760417 C36.2421905,19.6477597 39.5441143,20.1708521 42.3684437,18.9103691 C45.1927731,17.649886 47.0084685,14.8428276 47.0000295,11.75 C47.0000295,11.3946378 46.9030823,11.0460037 46.7199583,10.7414583 Z"></path>
                        <path class="color-background" d="M39.198,22.4912623 C37.3776246,22.4928106 35.5817531,22.0149171 33.951625,21.0951667 L33.92225,21.1107282 C31.1430221,22.6838032 27.9255001,22.9318916 24.9844167,21.7998837 C24.4750389,21.605469 23.9777983,21.3722567 23.4960833,21.1018359 L23.4745417,21.1129513 C20.6961809,22.6871153 17.4786145,22.9344611 14.5386667,21.7998837 C14.029926,21.6054643 13.533337,21.3722507 13.0522917,21.1018359 C11.4250962,22.0190609 9.63246555,22.4947009 7.81570833,22.4912623 C7.16510551,22.4842162 6.51607673,22.4173045 5.875,22.2911849 L5.875,44.7220845 C5.875,45.9498589 6.7517757,46.9451667 7.83333333,46.9451667 L19.5833333,46.9451667 L19.5833333,33.6066734 L27.4166667,33.6066734 L27.4166667,46.9451667 L39.1666667,46.9451667 C40.2482243,46.9451667 41.125,45.9498589 41.125,44.7220845 L41.125,22.2822926 C40.4887822,22.4116582 39.8442868,22.4815492 39.198,22.4912623 Z"></path>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
                        </div>
            <span class="nav-link-text ms-1">Home</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/dashboard?name={{display_name}}">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="15px" height="15px" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);transform: ;msFilter:;"><path d="M4 13h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1zm-1 7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v4zm10 0a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v7zm1-10h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1z"></path></svg>  
            </div>
            <span class="nav-link-text ms-1">Dashboard</span>
          </a>
        </li>

        <li class="nav-item">
        <a class="nav-link active" href="/cosmetics?name={{display_name}}">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="15px" height="15px" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(12, 12, 12, 1);transform: ;msFilter:;"><path class="color-background" d="M12 2a5 5 0 1 0 5 5 5 5 0 0 0-5-5zm0 8a3 3 0 1 1 3-3 3 3 0 0 1-3 3zm9 11v-1a7 7 0 0 0-7-7h-4a7 7 0 0 0-7 7v1h2v-1a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v1z"></path></svg>
          </div>
            <span class="nav-link-text ms-1">Cosmetics</span>
          </a>
          </li> 
          <li class="nav-item">
          <a class="nav-link" href="https://klldfn.xyz/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <i class="ni ni-world-2 text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
            </div>
            <span class="nav-link-text ms-1">Website</span>
          </a>

        </li>

      </ul>
    </div>
    <div class="sidenav-footer mx-3 ">
      <div class="card card-background shadow-none card-background-mask-dark" id="sidenavCard">
        <div class="full-background" style="background-image: url('https://klldfn-ui-dashboard.klldfn.xyz/assets/img/curved-images/white-curved.jpg')"></div>
        <div class="card-body text-start p-3 w-100">
          <div class="icon icon-shape icon-sm bg-white shadow text-center mb-3 d-flex align-items-center justify-content-center border-radius-md">
            <i class="ni ni-diamond text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
          </div>
          <div class="docs-info">
            <h6 class="text-white up mb-0">Need help?</h6>
            <p class="text-xs font-weight-bold">Enter the Discord server</p>
            <a href="https://discord.gg/ybr7evg4q5" target="_blank" class="btn btn-white btn-sm w-100 mb-0">link</a>
          </div>
        </div>
      </div>
    </div>

  </aside>
  <main class="main-content position-relative max-height-vh-100 h-100 border-radius-lg ">
    <!-- Navbar -->
    <nav class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl position-sticky blur shadow-blur mt-4 left-auto top-1 z-index-sticky" id="navbarBlur" navbar-scroll="true">
      <div class="container-fluid py-1 px-3">
        <nav aria-label="breadcrumb">
          <h6 class="font-weight-bolder mb-0">Dashboard</h6>
        </nav>
        <div class="collapse navbar-collapse mt-sm-0 mt-2 me-md-0 me-sm-4" id="navbar">

          <div class="ms-md-auto pe-md-3 d-flex align-items-center">
            <!--
            <div class="input-group">
              <span class="input-group-text text-body"><i class="fas fa-search" aria-hidden="true"></i></span>
              <input type="text" class="form-control" placeholder="Type here...">
            </div>
          </div>
          <ul class="navbar-nav  justify-content-end">

            <li class="nav-item d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body font-weight-bold px-0">
                <i class="fa fa-user me-sm-1"></i>
                <span class="d-sm-inline d-none">Sign In</span>
              </a>
            </li>
              -->
            <li class="nav-item d-xl-none ps-3 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" id="iconNavbarSidenav">
                <div class="sidenav-toggler-inner">
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                </div>
              </a>

            </li>

            <li class="nav-item px-3 d-flex align-items-center">
            </li>
            <!--
            <li class="nav-item dropdown pe-2 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fa fa-bell cursor-pointer"></i>
              </a>
              <ul class="dropdown-menu  dropdown-menu-end  px-2 py-3 me-sm-n4" aria-labelledby="dropdownMenuButton">
                <h6 class="text-sm font-weight-normal mb-1">
                  No New notifications
                </h6>
              </ul>
            </li>
            -->
          </ul>
        </div>
      </div>
    </nav>
    <!-- End Navbar -->
    <main class="main-content  mt-0">
      <section>
        <div class="page-header min-vh-75">
          <div class="container">
            <div class="row">
              <div class="col-xl-4 col-lg-5 col-md-6 d-flex flex-column mx-auto">
                <div class="card card-plain mt-8">
                  <div class="card-header pb-0 text-left bg-transparent">
                    <h3 class="font-weight-bolder text-info text-gradient">Fortnite Skin Selection</h3>
                    <div id="response">
                      {% if message %}
                      {% if icon_url %}
                      <img src="{{ icon_url }}" alt="Cosmetic Icon" class="w-100 border-radius-lg shadow-sm">
                      {% endif %}
                      <p class="mb-0">{{ message }}</p>
                      {% elif error %}
                          <p class="mb-0">{{ error }}</p>
                      {% endif %}
                  </div>
                  </div>
                  <div class="card-body">
                    <form action="?name={{ display_name }}" method="post">
                      <div class="mb-3">

                        <input type="text" class="form-control" placeholder="Enter Skin Name" id="skin" name="content">
                      </div>



                      <div class="text-center">
                        <input type="submit" class="btn bg-gradient-info w-100 mt-4 mb-0" value="Submit">
                      </div>
                    </form>
                  </div>

                </div>
              </div>

              </div>
            </div>
          </div>
        </div>
      </section>
    </main>


    <footer class="footer py-5">
      <div class="container">
        <div class="row">
        </div>
        <div class="row">
          <div class="col-8 mx-auto text-center mt-1">
            <p class="mb-0 text-secondary">
              Copyright © <script>
                document.write(new Date().getFullYear())
              </script>,
              <i class="fa fa-heart"></i> by
              klldFN
              All Right Reserved
            </p>
          </div>
        </div>
      </div>
    </footer>


  <!--   Core JS Files   -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/popper.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/bootstrap.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/perfect-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/smooth-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/chartjs.min.js"></script>


  <script>
    var ctx = document.getElementById("chart-bars").getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Sales",
          tension: 0.4,
          borderWidth: 0,
          borderRadius: 4,
          borderSkipped: false,
          backgroundColor: "#fff",
          data: [450, 200, 100, 220, 500, 100, 400, 230, 500],
          maxBarThickness: 6
        }, ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
            },
            ticks: {
              suggestedMin: 0,
              suggestedMax: 500,
              beginAtZero: true,
              padding: 15,
              font: {
                size: 14,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
              color: "#fff"
            },
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false
            },
            ticks: {
              display: false
            },
          },
        },
      },
    });


    var ctx2 = document.getElementById("chart-line").getContext("2d");

    var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke1.addColorStop(1, 'rgba(203,12,159,0.2)');
    gradientStroke1.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke1.addColorStop(0, 'rgba(203,12,159,0)'); //purple colors

    var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke2.addColorStop(1, 'rgba(20,23,39,0.2)');
    gradientStroke2.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke2.addColorStop(0, 'rgba(20,23,39,0)'); //purple colors

    new Chart(ctx2, {
      type: "line",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
            label: "Mobile apps",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#cb0c9f",
            borderWidth: 3,
            backgroundColor: gradientStroke1,
            fill: true,
            data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
            maxBarThickness: 6

          },
          {
            label: "Websites",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#3A416F",
            borderWidth: 3,
            backgroundColor: gradientStroke2,
            fill: true,
            data: [30, 90, 40, 140, 290, 290, 340, 230, 400],
            maxBarThickness: 6
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              padding: 10,
              color: '#b2b9bf',
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              color: '#b2b9bf',
              padding: 20,
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });
  </script>
  <script>
    var win = navigator.platform.indexOf('Win') > -1;
    if (win && document.querySelector('#sidenav-scrollbar')) {
      var options = {
        damping: '0.5'
      }
      Scrollbar.init(document.querySelector('#sidenav-scrollbar'), options);
    }
  </script>
  <script>
    // Simulate content loaded event
    window.addEventListener('load', function() {
      // Hide loading overlay after 3 seconds (adjust the duration as needed)
      setTimeout(function() {
        document.getElementById('loadingOverlay').style.display = 'none';
      }, 3000); // Duration in milliseconds (e.g., 3000 for 3 seconds)
    });
  </script>
  <!-- Github buttons -->
  <script async defer src="https://buttons.github.io/buttons.js"></script>
  <!-- Control Center for Soft Dashboard: parallax effects, scripts for the example pages etc -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz//assets/js/soft-ui-dashboard.min.js?v=1.0.7"></script>
</body>

</html>      
"""

@Sanic.route('/cosmetics/skin', methods=['GET', 'POST'])
async def skin_route(request):
        template = Template(template_html)
        client_name = request.args.get('name')
        try:
          client = [c for c in clients if c.user.display_name == client_name][0]
        except IndexError:
          return sanic.response.html("Client not found")
        if client:
          if request.method == 'GET':
            display_name_get = client.user.display_name
            return sanic.response.html(template.render(client_name=client_name, message=None, error=None, icon_url=None, display_name=display_name_get))
          elif request.method == 'POST':
            content = request.form.get('content')
            try:
                display_name_post = client.user.display_name
                cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language, matchMethod="contains", name=content, backendType="AthenaCharacter")
                await client.party.me.set_outfit(asset=cosmetic.id)
                skin_set = translations.read()["translations"]["skin-set"][get_Language]
                return sanic.response.html(template.render(client_name=client_name, message=skin_set.format(cosmetic.name), error=None, icon_url=f"https://fortnite-api.com/images/cosmetics/br/{cosmetic.id}/icon.png", display_name=display_name_post))      
            except FortniteAPIAsync.exceptions.NotFound:
                return sanic.response.html(template.render(client_name=client_name, message=None, error="Cosmetic not found", icon_url=None, display_name=display_name_post))
        else: 
          return sanic.response.html("Client not found")

template_html_emote = """
<!--
=========================================================
* klldFN UI Dashboard
=========================================================
-->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="apple-touch-icon" sizes="76x76" href="https://klldfn.xyz/icon.png">
  <link rel="icon" type="image/png" href="https://klldfn.xyz/icon.png">
  <title>
    klldFN Dashboard | Cosmetics
  </title>
  <!--     Fonts and icons     -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet" />
  <!-- Nucleo Icons -->
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-icons.css" rel="stylesheet" />
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-svg.css" rel="stylesheet" />
  <!-- Font Awesome Icons -->
  <script src="https://kit.fontawesome.com/42d5adcbca.js" crossorigin="anonymous"></script>
  <link href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/nucleo-svg.css" rel="stylesheet" />
  <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
  <!-- CSS Files -->
  <link id="pagestyle" href="https://klldfn-ui-dashboard.klldfn.xyz/assets/css/klldFN-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
  <!-- Nepcha Analytics (nepcha.com) -->
  <!-- Nepcha is a easy-to-use web analytics. No cookies and fully compliant with GDPR, CCPA and PECR. -->
  <script defer data-site="klldFN.xyz" src="https://api.nepcha.com/js/nepcha-analytics.js"></script>
  <style>
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(255, 255, 255, 0.8);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }

    .spinner-border {
      width: 3rem;
      height: 3rem;
    }
  </style>
</head>

<body class="g-sidenav-show  bg-gray-100">
  <div class="loading-overlay" id="loadingOverlay">
    <div class="spinner-border" role="status">

    </div>
  </div>

  <aside class="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3 bg-white" id="sidenav-main" data-color="dark">
    <div class="sidenav-header">
      <i class="fas fa-times p-3 cursor-pointer text-secondary opacity-5 position-absolute end-0 top-0 d-none d-xl-none" aria-hidden="true" id="iconSidenav"></i>
      <a class="navbar-brand m-0" href="#">
        <img src="https://klldfn.xyz/icon.png" class="navbar-brand-img h-100" alt="main_logo">
        <span class="ms-1 font-weight-bold">klldFN Dashboard</span>
      </a>
    </div>
    <hr class="horizontal dark mt-0">
    <div class="collapse navbar-collapse  w-auto " id="sidenav-collapse-main">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
            <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <path class="color-background opacity-6" d="M46.7199583,10.7414583 L40.8449583,0.949791667 C40.4909749,0.360605034 39.8540131,0 39.1666667,0 L7.83333333,0 C7.1459869,0 6.50902508,0.360605034 6.15504167,0.949791667 L0.280041667,10.7414583 C0.0969176761,11.0460037 -1.23209662e-05,11.3946378 -1.23209662e-05,11.75 C-0.00758042603,16.0663731 3.48367543,19.5725301 7.80004167,19.5833333 L7.81570833,19.5833333 C9.75003686,19.5882688 11.6168794,18.8726691 13.0522917,17.5760417 C16.0171492,20.2556967 20.5292675,20.2556967 23.494125,17.5760417 C26.4604562,20.2616016 30.9794188,20.2616016 33.94575,17.5760417 C36.2421905,19.6477597 39.5441143,20.1708521 42.3684437,18.9103691 C45.1927731,17.649886 47.0084685,14.8428276 47.0000295,11.75 C47.0000295,11.3946378 46.9030823,11.0460037 46.7199583,10.7414583 Z"></path>
                        <path class="color-background" d="M39.198,22.4912623 C37.3776246,22.4928106 35.5817531,22.0149171 33.951625,21.0951667 L33.92225,21.1107282 C31.1430221,22.6838032 27.9255001,22.9318916 24.9844167,21.7998837 C24.4750389,21.605469 23.9777983,21.3722567 23.4960833,21.1018359 L23.4745417,21.1129513 C20.6961809,22.6871153 17.4786145,22.9344611 14.5386667,21.7998837 C14.029926,21.6054643 13.533337,21.3722507 13.0522917,21.1018359 C11.4250962,22.0190609 9.63246555,22.4947009 7.81570833,22.4912623 C7.16510551,22.4842162 6.51607673,22.4173045 5.875,22.2911849 L5.875,44.7220845 C5.875,45.9498589 6.7517757,46.9451667 7.83333333,46.9451667 L19.5833333,46.9451667 L19.5833333,33.6066734 L27.4166667,33.6066734 L27.4166667,46.9451667 L39.1666667,46.9451667 C40.2482243,46.9451667 41.125,45.9498589 41.125,44.7220845 L41.125,22.2822926 C40.4887822,22.4116582 39.8442868,22.4815492 39.198,22.4912623 Z"></path>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
                        </div>
            <span class="nav-link-text ms-1">Home</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/dashboard?name={{display_name}}">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="15px" height="15px" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);transform: ;msFilter:;"><path d="M4 13h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1zm-1 7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v4zm10 0a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v7zm1-10h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1z"></path></svg>  
            </div>
            <span class="nav-link-text ms-1">Dashboard</span>
          </a>
        </li>

        <li class="nav-item">
        <a class="nav-link active" href="/cosmetics?name={{display_name}}">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="15px" height="15px" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(12, 12, 12, 1);transform: ;msFilter:;"><path class="color-background" d="M12 2a5 5 0 1 0 5 5 5 5 0 0 0-5-5zm0 8a3 3 0 1 1 3-3 3 3 0 0 1-3 3zm9 11v-1a7 7 0 0 0-7-7h-4a7 7 0 0 0-7 7v1h2v-1a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v1z"></path></svg>
          </div>
            <span class="nav-link-text ms-1">Cosmetics</span>
          </a>
          </li> 
          <li class="nav-item">
          <a class="nav-link" href="https://klldfn.xyz/">
            <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
              <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                    <g transform="translate(1716.000000, 291.000000)">
                      <g transform="translate(0.000000, 148.000000)">
                        <i class="ni ni-world-2 text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
                      </g>
                    </g>
                  </g>
                </g>
              </svg>
            </div>
            <span class="nav-link-text ms-1">Website</span>
          </a>

        </li>

      </ul>
    </div>
    <div class="sidenav-footer mx-3 ">
      <div class="card card-background shadow-none card-background-mask-dark" id="sidenavCard">
        <div class="full-background" style="background-image: url('https://klldfn-ui-dashboard.klldfn.xyz/assets/img/curved-images/white-curved.jpg')"></div>
        <div class="card-body text-start p-3 w-100">
          <div class="icon icon-shape icon-sm bg-white shadow text-center mb-3 d-flex align-items-center justify-content-center border-radius-md">
            <i class="ni ni-diamond text-dark text-gradient text-lg top-0" aria-hidden="true" id="sidenavCardIcon"></i>
          </div>
          <div class="docs-info">
            <h6 class="text-white up mb-0">Need help?</h6>
            <p class="text-xs font-weight-bold">Enter the Discord server</p>
            <a href="https://discord.gg/ybr7evg4q5" target="_blank" class="btn btn-white btn-sm w-100 mb-0">link</a>
          </div>
        </div>
      </div>
    </div>

  </aside>
  <main class="main-content position-relative max-height-vh-100 h-100 border-radius-lg ">
    <!-- Navbar -->
    <nav class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl position-sticky blur shadow-blur mt-4 left-auto top-1 z-index-sticky" id="navbarBlur" navbar-scroll="true">
      <div class="container-fluid py-1 px-3">
        <nav aria-label="breadcrumb">
          <h6 class="font-weight-bolder mb-0">Dashboard</h6>
        </nav>
        <div class="collapse navbar-collapse mt-sm-0 mt-2 me-md-0 me-sm-4" id="navbar">

          <div class="ms-md-auto pe-md-3 d-flex align-items-center">
            <!--
            <div class="input-group">
              <span class="input-group-text text-body"><i class="fas fa-search" aria-hidden="true"></i></span>
              <input type="text" class="form-control" placeholder="Type here...">
            </div>
          </div>
          <ul class="navbar-nav  justify-content-end">

            <li class="nav-item d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body font-weight-bold px-0">
                <i class="fa fa-user me-sm-1"></i>
                <span class="d-sm-inline d-none">Sign In</span>
              </a>
            </li>
              -->
            <li class="nav-item d-xl-none ps-3 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" id="iconNavbarSidenav">
                <div class="sidenav-toggler-inner">
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                </div>
              </a>

            </li>

            <li class="nav-item px-3 d-flex align-items-center">
            </li>
            <!--
            <li class="nav-item dropdown pe-2 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fa fa-bell cursor-pointer"></i>
              </a>
              <ul class="dropdown-menu  dropdown-menu-end  px-2 py-3 me-sm-n4" aria-labelledby="dropdownMenuButton">
                <h6 class="text-sm font-weight-normal mb-1">
                  No New notifications
                </h6>
              </ul>
            </li>
            -->
          </ul>
        </div>
      </div>
    </nav>
    <!-- End Navbar -->
    <main class="main-content  mt-0">
      <section>
        <div class="page-header min-vh-75">
          <div class="container">
            <div class="row">
              <div class="col-xl-4 col-lg-5 col-md-6 d-flex flex-column mx-auto">
                <div class="card card-plain mt-8">
                  <div class="card-header pb-0 text-left bg-transparent">
                    <h3 class="font-weight-bolder text-info text-gradient">Fortnite Emote Selection</h3>
                    <div id="response">
                      {% if message %}
                      {% if icon_url %}
                          <img src="{{ icon_url }}" alt="Cosmetic Icon" class="w-100 border-radius-lg shadow-sm">
                      {% endif %}
                          <p class="mb-0">{{ message }}</p>
                      {% elif error %}
                          <p class="mb-0">{{ error }}</p>
                      {% endif %}
                  </div>
                  </div>
                  <div class="card-body">
                    <form action="?name={{ display_name }}" method="post">
                      <div class="mb-3">

                        <input type="text" class="form-control" placeholder="Enter Emote Name" id="emote" name="content">
                      </div>



                      <div class="text-center">
                        <input type="submit" class="btn bg-gradient-info w-100 mt-4 mb-0" value="Submit">
                      </div>
                    </form>
                  </div>

                </div>
              </div>

              </div>
            </div>
          </div>
        </div>
      </section>
    </main>


    <footer class="footer py-5">
      <div class="container">
        <div class="row">
        </div>
        <div class="row">
          <div class="col-8 mx-auto text-center mt-1">
            <p class="mb-0 text-secondary">
              Copyright © <script>
                document.write(new Date().getFullYear())
              </script>,
              <i class="fa fa-heart"></i> by
              klldFN
              All Right Reserved
            </p>
          </div>
        </div>
      </div>
    </footer>


  <!--   Core JS Files   -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/popper.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/core/bootstrap.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/perfect-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/smooth-scrollbar.min.js"></script>
  <script src="https://klldfn-ui-dashboard.klldfn.xyz/assets/js/plugins/chartjs.min.js"></script>


  <script>
    var ctx = document.getElementById("chart-bars").getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Sales",
          tension: 0.4,
          borderWidth: 0,
          borderRadius: 4,
          borderSkipped: false,
          backgroundColor: "#fff",
          data: [450, 200, 100, 220, 500, 100, 400, 230, 500],
          maxBarThickness: 6
        }, ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
            },
            ticks: {
              suggestedMin: 0,
              suggestedMax: 500,
              beginAtZero: true,
              padding: 15,
              font: {
                size: 14,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
              color: "#fff"
            },
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false
            },
            ticks: {
              display: false
            },
          },
        },
      },
    });


    var ctx2 = document.getElementById("chart-line").getContext("2d");

    var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke1.addColorStop(1, 'rgba(203,12,159,0.2)');
    gradientStroke1.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke1.addColorStop(0, 'rgba(203,12,159,0)'); //purple colors

    var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

    gradientStroke2.addColorStop(1, 'rgba(20,23,39,0.2)');
    gradientStroke2.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke2.addColorStop(0, 'rgba(20,23,39,0)'); //purple colors

    new Chart(ctx2, {
      type: "line",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
            label: "Mobile apps",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#cb0c9f",
            borderWidth: 3,
            backgroundColor: gradientStroke1,
            fill: true,
            data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
            maxBarThickness: 6

          },
          {
            label: "Websites",
            tension: 0.4,
            borderWidth: 0,
            pointRadius: 0,
            borderColor: "#3A416F",
            borderWidth: 3,
            backgroundColor: gradientStroke2,
            fill: true,
            data: [30, 90, 40, 140, 290, 290, 340, 230, 400],
            maxBarThickness: 6
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              padding: 10,
              color: '#b2b9bf',
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              color: '#b2b9bf',
              padding: 20,
              font: {
                size: 11,
                family: "Open Sans",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });
  </script>
  <script>
    var win = navigator.platform.indexOf('Win') > -1;
    if (win && document.querySelector('#sidenav-scrollbar')) {
      var options = {
        damping: '0.5'
      }
      Scrollbar.init(document.querySelector('#sidenav-scrollbar'), options);
    }
  </script>
  <script>
    // Simulate content loaded event
    window.addEventListener('load', function() {
      // Hide loading overlay after 3 seconds (adjust the duration as needed)
      setTimeout(function() {
        document.getElementById('loadingOverlay').style.display = 'none';
      }, 3000); // Duration in milliseconds (e.g., 3000 for 3 seconds)
    });
  </script>
  <!-- Github buttons -->
  <script async defer src="https://buttons.github.io/buttons.js"></script>
  <!-- Control Center for Soft Dashboard: parallax effects, scripts for the example pages etc -->
  <script src="https://klldfn-ui-dashboard.klldfn.xyz//assets/js/soft-ui-dashboard.min.js?v=1.0.7"></script>
</body>

</html>
"""

@Sanic.route('/cosmetics/emote', methods=['GET', 'POST'])
async def emote_route(request):
        template_emote = Template(template_html_emote)
        client_name = request.args.get('name')
        try:
            client = [c for c in clients if c.user.display_name == client_name][0]
        except IndexError:
            return sanic.response.html("Client not found")
        if client:
          if request.method == 'GET':
            display_name_get = client.user.display_name
            return sanic.response.html(template_emote.render(client_name=client_name, message=None, error=None, icon_url=None, display_name=display_name_get))
          elif request.method == 'POST':
            content = request.form.get('content')
            try:
                cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language, matchMethod="contains", name=content, backendType="AthenaDance")
                await client.party.me.set_emote(asset=cosmetic.id)
                emote_set = translations.read()["translations"]["emote-set"][get_Language]
                display_name_post = client.user.display_name
                return sanic.response.html(template_emote.render(client_name=client_name, message=emote_set.format(cosmetic.name), error=None, icon_url=f"https://fortnite-api.com/images/cosmetics/br/{cosmetic.id}/icon.png", display_name=display_name_post))      
            except FortniteAPIAsync.exceptions.NotFound:
                return sanic.response.html(template_emote.render(client_name=client_name, message=None, error="Cosmetic not found", icon_url=None, display_name=display_name_get))
        else:
          return sanic.response.html("Client not found")

# Run the clients

asyncio.run(clients_sanic_Run())

