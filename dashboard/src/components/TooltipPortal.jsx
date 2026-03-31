import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';

export function TooltipPortal({ anchorRef, children, visible }) {
  const [coords, setCoords] = useState({ top: 0, left: 0 });

  useEffect(() => {
    if (anchorRef.current && visible) {
      const rect = anchorRef.current.getBoundingClientRect();
      setCoords({
        top: rect.bottom + window.scrollY + 6,
        left: rect.left + window.scrollX + rect.width / 2,
      });
    }
  }, [anchorRef, visible]);

  if (!visible) return null;

  return createPortal(
    <div
      role="tooltip"
      style={{
        position: 'absolute',
        top: coords.top,
        left: coords.left,
        transform: 'translateX(-50%)',
        background: '#222',
        color: '#fff',
        padding: '6px 10px',
        borderRadius: 4,
        fontSize: '0.85em',
        whiteSpace: 'pre-line',
        zIndex: 9999,
        minWidth: 180,
        maxWidth: 260,
        boxShadow: '0 2px 8px rgba(0,0,0,0.18)',
        pointerEvents: 'auto',
        animation: 'fade-in-tooltip 0.18s cubic-bezier(0.4,0,0.2,1)',
      }}
      className="header-tooltip-text-portal"
    >
      {children}
    </div>,
    document.body
  );
}
