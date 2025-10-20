#!/usr/bin/env python3
"""
Channel Management CLI Tool for Content Generator 3000

This tool allows you to manage YouTube channels in your configuration.
"""

import argparse
import sys
from utils.config import ConfigManager


def list_channels(config: ConfigManager, all_channels: bool = False):
    """List all channels in the configuration."""
    channels = config.get_channels(enabled_only=not all_channels)

    if not channels:
        print("No channels configured.")
        return

    print("\n" + "="*80)
    print(f"{'ID':<30} {'Name':<30} {'Status':<10}")
    print("="*80)

    for channel in channels:
        channel_id = channel.get('id', 'N/A')
        name = channel.get('name', 'Unnamed')
        enabled = channel.get('enabled', True)
        status = "Enabled" if enabled else "Disabled"

        print(f"{channel_id:<30} {name:<30} {status:<10}")

    print("="*80)
    print(f"Total: {len(channels)} channel(s)")

    if not all_channels:
        print("\nShowing enabled channels only. Use --all to see all channels.")
    print()


def add_channel(config: ConfigManager, channel_id: str, name: str, enabled: bool):
    """Add a new channel to the configuration."""
    if config.add_channel(channel_id, name, enabled):
        status = "enabled" if enabled else "disabled"
        print(f"\nSuccessfully added channel '{name}' ({channel_id}) - {status}")
        print("Channel has been saved to config.yaml")
    else:
        print(f"\nError: Channel with ID '{channel_id}' already exists.")
        sys.exit(1)


def remove_channel(config: ConfigManager, channel_id: str):
    """Remove a channel from the configuration."""
    if config.remove_channel(channel_id):
        print(f"\nSuccessfully removed channel: {channel_id}")
        print("Changes have been saved to config.yaml")
    else:
        print(f"\nError: Channel with ID '{channel_id}' not found.")
        sys.exit(1)


def enable_channel(config: ConfigManager, channel_id: str):
    """Enable a channel."""
    if config.enable_channel(channel_id):
        print(f"\nSuccessfully enabled channel: {channel_id}")
        print("Changes have been saved to config.yaml")
    else:
        print(f"\nError: Channel with ID '{channel_id}' not found.")
        sys.exit(1)


def disable_channel(config: ConfigManager, channel_id: str):
    """Disable a channel."""
    if config.disable_channel(channel_id):
        print(f"\nSuccessfully disabled channel: {channel_id}")
        print("Changes have been saved to config.yaml")
    else:
        print(f"\nError: Channel with ID '{channel_id}' not found.")
        sys.exit(1)


def rename_channel(config: ConfigManager, channel_id: str, name: str):
    """Update a channel's name."""
    if config.update_channel_name(channel_id, name):
        print(f"\nSuccessfully renamed channel {channel_id} to '{name}'")
        print("Changes have been saved to config.yaml")
    else:
        print(f"\nError: Channel with ID '{channel_id}' not found.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Manage YouTube channels for Content Generator 3000",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                                    List all enabled channels
  %(prog)s list --all                             List all channels (including disabled)
  %(prog)s add UCxxxxxx "AI News Channel"          Add a new channel
  %(prog)s add UCxxxxxx "Test Channel" --disabled  Add a disabled channel
  %(prog)s remove UCxxxxxx                         Remove a channel
  %(prog)s enable UCxxxxxx                         Enable a channel
  %(prog)s disable UCxxxxxx                        Disable a channel
  %(prog)s rename UCxxxxxx "New Channel Name"      Rename a channel
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    list_parser = subparsers.add_parser('list', help='List all channels')
    list_parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Show all channels including disabled ones'
    )

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new channel')
    add_parser.add_argument('channel_id', help='YouTube channel ID')
    add_parser.add_argument('name', help='Channel name/description')
    add_parser.add_argument(
        '--disabled',
        action='store_true',
        help='Add channel in disabled state'
    )

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a channel')
    remove_parser.add_argument('channel_id', help='YouTube channel ID to remove')

    # Enable command
    enable_parser = subparsers.add_parser('enable', help='Enable a channel')
    enable_parser.add_argument('channel_id', help='YouTube channel ID to enable')

    # Disable command
    disable_parser = subparsers.add_parser('disable', help='Disable a channel')
    disable_parser.add_argument('channel_id', help='YouTube channel ID to disable')

    # Rename command
    rename_parser = subparsers.add_parser('rename', help='Rename a channel')
    rename_parser.add_argument('channel_id', help='YouTube channel ID to rename')
    rename_parser.add_argument('name', help='New name for the channel')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        config = ConfigManager()
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nPlease create a config.yaml file based on config.example.yaml")
        sys.exit(1)
    except Exception as e:
        print(f"\nError loading configuration: {e}")
        sys.exit(1)

    # Execute command
    if args.command == 'list':
        list_channels(config, args.all)
    elif args.command == 'add':
        add_channel(config, args.channel_id, args.name, not args.disabled)
    elif args.command == 'remove':
        remove_channel(config, args.channel_id)
    elif args.command == 'enable':
        enable_channel(config, args.channel_id)
    elif args.command == 'disable':
        disable_channel(config, args.channel_id)
    elif args.command == 'rename':
        rename_channel(config, args.channel_id, args.name)


if __name__ == '__main__':
    main()
