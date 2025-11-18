"""
Professional Text Formatter for EduBot
Provides beautiful, consistent formatting for bot responses
"""


class TextFormatter:
    """Format bot responses with professional styling"""
    
    # Color-coded emoji categories
    ICONS = {
        'success': '✅',
        'info': 'ℹ️',
        'warning': '⚠️',
        'error': '❌',
        'tip': '💡',
        'academic': '📚',
        'calendar': '📅',
        'time': '⏰',
        'location': '📍',
        'phone': '📞',
        'email': '📧',
        'web': '🌐',
        'star': '⭐',
        'trophy': '🏆',
        'rocket': '🚀',
        'fire': '🔥',
        'money': '💰',
        'book': '📖',
        'pencil': '✏️',
        'graduation': '🎓',
        'computer': '💻',
        'science': '🔬',
        'math': '🧮',
        'art': '🎨',
        'music': '🎵',
        'sports': '⚽',
        'food': '🍽️',
        'bus': '🚌',
        'building': '🏛️'
    }
    
    @staticmethod
    def header(text, style='bold'):
        """Create a header"""
        if style == 'bold':
            return f"\n{'═' * 50}\n  {text.upper()}\n{'═' * 50}\n"
        elif style == 'simple':
            return f"\n━━━ {text} ━━━\n"
        elif style == 'box':
            line = '─' * (len(text) + 4)
            return f"\n┌{line}┐\n│  {text}  │\n└{line}┘\n"
    
    @staticmethod
    def section(title, content, icon=None):
        """Create a formatted section"""
        icon_str = f"{icon} " if icon else ""
        return f"\n{icon_str}**{title}**\n{content}\n"
    
    @staticmethod
    def list_items(items, style='bullet', icon=None):
        """Format a list of items"""
        if not items:
            return ""
        
        formatted = []
        for i, item in enumerate(items, 1):
            if style == 'bullet':
                prefix = f"  • {icon} " if icon else "  • "
            elif style == 'numbered':
                prefix = f"  {i}. "
            elif style == 'checkbox':
                prefix = "  ☐ "
            elif style == 'checked':
                prefix = "  ✓ "
            else:
                prefix = "  → "
            
            formatted.append(f"{prefix}{item}")
        
        return "\n".join(formatted)
    
    @staticmethod
    def key_value(data, separator=':', indent=2):
        """Format key-value pairs"""
        if not data:
            return ""
        
        formatted = []
        indent_str = " " * indent
        max_key_len = max(len(str(k)) for k in data.keys())
        
        for key, value in data.items():
            key_padded = str(key).ljust(max_key_len)
            formatted.append(f"{indent_str}{key_padded} {separator} {value}")
        
        return "\n".join(formatted)
    
    @staticmethod
    def table(headers, rows):
        """Create a simple text table"""
        if not rows:
            return ""
        
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Create header
        header_line = "  " + " │ ".join(h.ljust(w) for h, w in zip(headers, col_widths))
        separator = "  " + "─" * len(header_line.strip())
        
        # Create rows
        table_rows = []
        for row in rows:
            row_line = "  " + " │ ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
            table_rows.append(row_line)
        
        return f"\n{header_line}\n{separator}\n" + "\n".join(table_rows) + "\n"
    
    @staticmethod
    def card(title, content, icon=None, footer=None):
        """Create a card-style message"""
        width = 50
        icon_str = f"{icon} " if icon else ""
        
        lines = [
            "┌" + "─" * (width - 2) + "┐",
            f"│ {icon_str}{title.upper()}".ljust(width - 1) + "│",
            "├" + "─" * (width - 2) + "┤"
        ]
        
        # Add content lines
        for line in content.split('\n'):
            if line:
                lines.append(f"│ {line}".ljust(width - 1) + "│")
        
        if footer:
            lines.extend([
                "├" + "─" * (width - 2) + "┤",
                f"│ {footer}".ljust(width - 1) + "│"
            ])
        
        lines.append("└" + "─" * (width - 2) + "┘")
        
        return "\n" + "\n".join(lines) + "\n"
    
    @staticmethod
    def highlight(text, style='bold'):
        """Highlight important text"""
        if style == 'bold':
            return f"**{text}**"
        elif style == 'italic':
            return f"*{text}*"
        elif style == 'code':
            return f"`{text}`"
        elif style == 'quote':
            return f"> {text}"
        return text
    
    @staticmethod
    def badge(text, color='blue'):
        """Create a badge-style label"""
        colors = {
            'blue': '🔵',
            'green': '🟢',
            'red': '🔴',
            'yellow': '🟡',
            'purple': '🟣'
        }
        icon = colors.get(color, '⚪')
        return f"{icon} {text}"
    
    @staticmethod
    def progress_bar(percentage, width=20):
        """Create a text progress bar"""
        filled = int(width * percentage / 100)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        return f"[{bar}] {percentage}%"
    
    @staticmethod
    def alert(message, type='info'):
        """Create an alert box"""
        icons = {
            'info': '💙 INFO',
            'success': '💚 SUCCESS',
            'warning': '💛 WARNING',
            'error': '❤️ ERROR',
            'tip': '💡 TIP'
        }
        
        icon = icons.get(type, '📢 NOTICE')
        border = "═" * 50
        
        return f"\n{border}\n{icon}\n{border}\n{message}\n{border}\n"
    
    @staticmethod
    def step_by_step(steps):
        """Format step-by-step instructions"""
        formatted = ["\n📋 **STEP-BY-STEP GUIDE**\n"]
        
        for i, step in enumerate(steps, 1):
            formatted.append(f"▶️ **Step {i}:** {step}")
        
        return "\n".join(formatted) + "\n"
    
    @staticmethod
    def quick_buttons(buttons):
        """Format quick action buttons"""
        button_lines = []
        for btn in buttons:
            button_lines.append(f"[ {btn} ]")
        
        return "\n🔘 Quick Actions: " + "  ".join(button_lines) + "\n"
    
    @staticmethod
    def contact_card(name, role=None, email=None, phone=None, office=None):
        """Format contact information"""
        lines = [f"\n👤 **{name}**"]
        
        if role:
            lines.append(f"   🎓 {role}")
        if email:
            lines.append(f"   📧 {email}")
        if phone:
            lines.append(f"   📞 {phone}")
        if office:
            lines.append(f"   📍 {office}")
        
        return "\n".join(lines) + "\n"
    
    @staticmethod
    def schedule_item(time, title, location=None, details=None):
        """Format a schedule/event item"""
        lines = [f"\n⏰ **{time}** - {title}"]
        
        if location:
            lines.append(f"   📍 {location}")
        if details:
            lines.append(f"   ℹ️ {details}")
        
        return "\n".join(lines)


# Quick formatting functions
def fmt_header(text):
    """Quick header"""
    return TextFormatter.header(text, 'simple')

def fmt_list(items, icon=None):
    """Quick bullet list"""
    return TextFormatter.list_items(items, 'bullet', icon)

def fmt_success(text):
    """Quick success message"""
    return f"✅ {text}"

def fmt_info(text):
    """Quick info message"""
    return f"ℹ️ {text}"

def fmt_warning(text):
    """Quick warning message"""
    return f"⚠️ {text}"
