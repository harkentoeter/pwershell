@bot.command(name="tp")  # Command: $tp
async def take_picture_command(ctx):
    file_path, message = take_picture()
    
    if file_path:
        await ctx.send("Picture taken:", file=discord.File(file_path))
    else:
        await ctx.send(f"Error: {message}")
