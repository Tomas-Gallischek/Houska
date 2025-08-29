def weapons_generator(username):
    print("Weapon generator SPUŠTĚNÝ")

    # Zde je logika tvého algoritmu, která využívá data z databáze
    try:
        player_info = Playerinfo.objects.get(username=username)
        # Zde budeš pracovat s daty z player_info
        print(f"Generuji zbraně pro uživatele: {player_info.username}")
        # ... zde tvůj algoritmus ...
        return f"Zbraně pro {player_info.username} byly vygenerovány."
    except Playerinfo.DoesNotExist:
        return f"Uživatel {username} nebyl nalezen."

# Spuštění testu s konkrétním uživatelem
test_user = 'Ewill'
result = weapons_generator(test_user)
print(result)