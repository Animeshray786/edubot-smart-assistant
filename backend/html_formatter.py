"""
Enhanced HTML Formatter for EduBot
Provides beautiful HTML-formatted responses for professional display
"""


class HTMLFormatter:
    """Format bot responses with professional HTML styling"""
    
    # Color schemes
    COLORS = {
        'primary': '#6366f1',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'info': '#3b82f6',
        'purple': '#a855f7',
        'pink': '#ec4899',
        'gradient_blue': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient_green': 'linear-gradient(135deg, #667eea 0%, #10b981 100%)',
        'gradient_orange': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'gradient_purple': 'linear-gradient(135deg, #a855f7 0%, #ec4899 100%)',
    }
    
    @staticmethod
    def header(text, color='primary', gradient=False):
        """Create an HTML header with gradient background"""
        bg = HTMLFormatter.COLORS.get(f'gradient_{color}', HTMLFormatter.COLORS[color])
        if not gradient:
            bg = HTMLFormatter.COLORS[color]
        
        return f"""
        <div style="background: {bg}; color: white; padding: 1rem 1.5rem; border-radius: 12px; 
                    margin: 1rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-weight: 600;">
            {text}
        </div>
        """
    
    @staticmethod
    def card(title, content, icon=None, color='primary'):
        """Create a styled card with optional icon"""
        icon_html = f'<span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>' if icon else ''
        border_color = HTMLFormatter.COLORS[color]
        
        return f"""
        <div style="border-left: 4px solid {border_color}; padding: 1rem; 
                    background: #f9fafb; border-radius: 8px; margin: 1rem 0;">
            <div style="font-weight: 600; color: {border_color}; margin-bottom: 0.5rem; font-size: 1.1rem;">
                {icon_html}{title}
            </div>
            <div style="color: #374151; line-height: 1.6;">
                {content}
            </div>
        </div>
        """
    
    @staticmethod
    def list_items(items, style='bullet', ordered=False, color='primary'):
        """Create a styled list"""
        list_type = 'ol' if ordered else 'ul'
        list_style = 'decimal' if ordered else 'disc'
        
        items_html = ''.join([
            f'<li style="margin-bottom: 0.5rem; line-height: 1.6;">{item}</li>' 
            for item in items
        ])
        
        return f"""
        <{list_type} style="list-style-type: {list_style}; padding-left: 1.5rem; 
                           color: #374151; margin: 0.5rem 0;">
            {items_html}
        </{list_type}>
        """
    
    @staticmethod
    def table(headers, rows, striped=True):
        """Create a styled HTML table"""
        header_html = ''.join([
            f'<th style="padding: 0.75rem; text-align: left; background: #6366f1; color: white; font-weight: 600;">{h}</th>'
            for h in headers
        ])
        
        rows_html = ''
        for i, row in enumerate(rows):
            bg_color = '#f9fafb' if striped and i % 2 == 0 else 'white'
            cells = ''.join([
                f'<td style="padding: 0.75rem; border-bottom: 1px solid #e5e7eb;">{cell}</td>'
                for cell in row
            ])
            rows_html += f'<tr style="background: {bg_color};">{cells}</tr>'
        
        return f"""
        <table style="width: 100%; border-collapse: collapse; margin: 1rem 0; 
                      border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <thead>
                <tr>{header_html}</tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
    
    @staticmethod
    def key_value(data, columns=1):
        """Create a styled key-value display"""
        items_html = ''
        for key, value in data.items():
            items_html += f"""
            <div style="display: flex; padding: 0.5rem 0; border-bottom: 1px solid #e5e7eb;">
                <div style="flex: 0 0 40%; font-weight: 600; color: #6366f1;">{key}:</div>
                <div style="flex: 1; color: #374151;">{value}</div>
            </div>
            """
        
        return f"""
        <div style="background: white; border-radius: 8px; padding: 1rem; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 1rem 0;">
            {items_html}
        </div>
        """
    
    @staticmethod
    def badge(text, color='primary'):
        """Create a colored badge"""
        bg_color = HTMLFormatter.COLORS[color]
        return f"""
        <span style="display: inline-block; padding: 0.25rem 0.75rem; 
                     background: {bg_color}; color: white; border-radius: 12px; 
                     font-size: 0.875rem; font-weight: 500; margin: 0.25rem;">
            {text}
        </span>
        """
    
    @staticmethod
    def alert(message, type='info', dismissible=False):
        """Create an alert box"""
        colors = {
            'info': ('#3b82f6', '#dbeafe'),
            'success': ('#10b981', '#d1fae5'),
            'warning': ('#f59e0b', '#fef3c7'),
            'danger': ('#ef4444', '#fee2e2')
        }
        
        border_color, bg_color = colors.get(type, colors['info'])
        
        icons = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'danger': '❌'
        }
        
        icon = icons.get(type, 'ℹ️')
        
        return f"""
        <div style="border-left: 4px solid {border_color}; background: {bg_color}; 
                    padding: 1rem; border-radius: 8px; margin: 1rem 0; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
            <span style="color: #374151; line-height: 1.6;">{message}</span>
        </div>
        """
    
    @staticmethod
    def progress_bar(percentage, label='', color='primary'):
        """Create a progress bar"""
        bg_color = HTMLFormatter.COLORS[color]
        
        return f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #374151; font-weight: 500;">{label}</span>
                <span style="color: {bg_color}; font-weight: 600;">{percentage}%</span>
            </div>
            <div style="width: 100%; background: #e5e7eb; border-radius: 12px; overflow: hidden; height: 8px;">
                <div style="width: {percentage}%; background: {bg_color}; height: 100%; 
                            transition: width 0.3s ease;"></div>
            </div>
        </div>
        """
    
    @staticmethod
    def timeline(events):
        """Create a timeline display"""
        timeline_html = ''
        for i, event in enumerate(events):
            is_last = i == len(events) - 1
            connector = '' if is_last else '<div style="width: 2px; height: 40px; background: #e5e7eb; margin-left: 15px;"></div>'
            
            timeline_html += f"""
            <div style="display: flex; margin-bottom: 0.5rem;">
                <div style="flex: 0 0 auto; margin-right: 1rem;">
                    <div style="width: 32px; height: 32px; background: #6366f1; 
                                border-radius: 50%; display: flex; align-items: center; 
                                justify-content: center; color: white; font-weight: 600;">
                        {i+1}
                    </div>
                </div>
                <div style="flex: 1; padding-bottom: 1rem;">
                    <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">
                        {event.get('title', '')}
                    </div>
                    <div style="color: #6b7280; font-size: 0.9rem;">
                        {event.get('description', '')}
                    </div>
                </div>
            </div>
            {connector}
            """
        
        return f"""
        <div style="padding: 1rem; margin: 1rem 0;">
            {timeline_html}
        </div>
        """
    
    @staticmethod
    def grid(items, columns=2):
        """Create a responsive grid layout"""
        items_html = ''.join([
            f"""
            <div style="padding: 1rem; background: white; border-radius: 8px; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                {item}
            </div>
            """
            for item in items
        ])
        
        return f"""
        <div style="display: grid; grid-template-columns: repeat({columns}, 1fr); 
                    gap: 1rem; margin: 1rem 0;">
            {items_html}
        </div>
        """
    
    @staticmethod
    def stats_card(value, label, icon=None, color='primary'):
        """Create a statistics card"""
        icon_html = f'<div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''
        text_color = HTMLFormatter.COLORS[color]
        
        return f"""
        <div style="padding: 1.5rem; background: white; border-radius: 12px; 
                    text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            {icon_html}
            <div style="font-size: 2rem; font-weight: 700; color: {text_color}; margin-bottom: 0.25rem;">
                {value}
            </div>
            <div style="color: #6b7280; font-size: 0.9rem;">
                {label}
            </div>
        </div>
        """
    
    @staticmethod
    def collapsible(title, content, expanded=False):
        """Create a collapsible section (note: requires JavaScript on frontend)"""
        return f"""
        <details style="margin: 1rem 0; border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem;" {'open' if expanded else ''}>
            <summary style="cursor: pointer; font-weight: 600; color: #6366f1; margin-bottom: 0.5rem;">
                {title}
            </summary>
            <div style="margin-top: 0.5rem; color: #374151; line-height: 1.6;">
                {content}
            </div>
        </details>
        """
    
    @staticmethod
    def button(text, url='#', color='primary', style='solid'):
        """Create a styled button link"""
        bg_color = HTMLFormatter.COLORS[color]
        
        if style == 'outline':
            styles = f"border: 2px solid {bg_color}; color: {bg_color}; background: transparent;"
        else:
            styles = f"background: {bg_color}; color: white; border: none;"
        
        return f"""
        <a href="{url}" style="display: inline-block; padding: 0.75rem 1.5rem; 
                                {styles} border-radius: 8px; text-decoration: none; 
                                font-weight: 600; margin: 0.5rem 0.5rem 0.5rem 0; 
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
                                transition: transform 0.2s;">
            {text}
        </a>
        """
    
    @staticmethod
    def section(title, content, icon=None, collapsible=False):
        """Create a formatted section with optional collapse"""
        icon_html = f'<span style="margin-right: 0.5rem;">{icon}</span>' if icon else ''
        
        if collapsible:
            return HTMLFormatter.collapsible(f"{icon_html}{title}", content)
        
        return f"""
        <div style="margin: 1.5rem 0;">
            <h3 style="color: #1f2937; font-size: 1.25rem; font-weight: 600; 
                       margin-bottom: 1rem; border-bottom: 2px solid #e5e7eb; 
                       padding-bottom: 0.5rem;">
                {icon_html}{title}
            </h3>
            <div style="color: #374151; line-height: 1.6;">
                {content}
            </div>
        </div>
        """


# Convenience functions
def fmt_card(title, content, icon=None, color='primary'):
    return HTMLFormatter.card(title, content, icon, color)

def fmt_header(text, color='primary', gradient=True):
    return HTMLFormatter.header(text, color, gradient)

def fmt_list(items, ordered=False):
    return HTMLFormatter.list_items(items, ordered=ordered)

def fmt_table(headers, rows):
    return HTMLFormatter.table(headers, rows)

def fmt_alert(message, type='info'):
    return HTMLFormatter.alert(message, type)

def fmt_badge(text, color='primary'):
    return HTMLFormatter.badge(text, color)

def fmt_progress(percentage, label='', color='primary'):
    return HTMLFormatter.progress_bar(percentage, label, color)

def fmt_button(text, url='#', color='primary'):
    return HTMLFormatter.button(text, url, color)
