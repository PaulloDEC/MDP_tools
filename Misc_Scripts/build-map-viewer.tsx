import React, { useState, useRef, useEffect } from 'react';
import { Upload, ZoomIn, ZoomOut, Home, Info } from 'lucide-react';

const BuildMapViewer = () => {
  const [mapData, setMapData] = useState(null);
  const [error, setError] = useState(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [hoverInfo, setHoverInfo] = useState(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  const parseMapFile = (buffer) => {
    const view = new DataView(buffer);
    let offset = 0;

    // Read header
    const version = view.getInt32(offset, true); offset += 4;
    const startx = view.getInt32(offset, true); offset += 4;
    const starty = view.getInt32(offset, true); offset += 4;
    const startz = view.getInt32(offset, true); offset += 4;
    const startang = view.getInt16(offset, true); offset += 2;
    const startsector = view.getInt16(offset, true); offset += 2;

    // Read sector count and sectors
    const numsectors = view.getInt16(offset, true); offset += 2;
    const sectors = [];
    
    for (let i = 0; i < numsectors; i++) {
      sectors.push({
        wallptr: view.getInt16(offset, true),
        wallnum: view.getInt16(offset + 2, true),
        ceilingz: view.getInt32(offset + 4, true),
        floorz: view.getInt32(offset + 8, true),
        ceilingstat: view.getInt16(offset + 12, true),
        floorstat: view.getInt16(offset + 14, true),
        ceilingpicnum: view.getInt16(offset + 16, true),
        ceilingheinum: view.getInt16(offset + 18, true),
        ceilingshade: view.getInt8(offset + 20),
        ceilingpal: view.getUint8(offset + 21),
        ceilingxpanning: view.getUint8(offset + 22),
        ceilingypanning: view.getUint8(offset + 23),
        floorpicnum: view.getInt16(offset + 24, true),
        floorheinum: view.getInt16(offset + 26, true),
        floorshade: view.getInt8(offset + 28),
        floorpal: view.getUint8(offset + 29),
        floorxpanning: view.getUint8(offset + 30),
        floorypanning: view.getUint8(offset + 31),
        visibility: view.getUint8(offset + 32),
        filler: view.getUint8(offset + 33),
        lotag: view.getInt16(offset + 34, true),
        hitag: view.getInt16(offset + 36, true),
        extra: view.getInt16(offset + 38, true)
      });
      offset += 40;
    }

    // Read wall count and walls
    const numwalls = view.getInt16(offset, true); offset += 2;
    const walls = [];
    
    for (let i = 0; i < numwalls; i++) {
      walls.push({
        x: view.getInt32(offset, true),
        y: view.getInt32(offset + 4, true),
        point2: view.getInt16(offset + 8, true),
        nextwall: view.getInt16(offset + 10, true),
        nextsector: view.getInt16(offset + 12, true),
        cstat: view.getInt16(offset + 14, true),
        picnum: view.getInt16(offset + 16, true),
        overpicnum: view.getInt16(offset + 18, true),
        shade: view.getInt8(offset + 20),
        pal: view.getUint8(offset + 21),
        xrepeat: view.getUint8(offset + 22),
        yrepeat: view.getUint8(offset + 23),
        xpanning: view.getUint8(offset + 24),
        ypanning: view.getUint8(offset + 25),
        lotag: view.getInt16(offset + 26, true),
        hitag: view.getInt16(offset + 28, true),
        extra: view.getInt16(offset + 30, true)
      });
      offset += 32;
    }

    // Read sprite count and sprites
    const numsprites = view.getInt16(offset, true); offset += 2;
    const sprites = [];
    
    for (let i = 0; i < numsprites; i++) {
      sprites.push({
        x: view.getInt32(offset, true),
        y: view.getInt32(offset + 4, true),
        z: view.getInt32(offset + 8, true),
        cstat: view.getInt16(offset + 12, true),
        picnum: view.getInt16(offset + 14, true),
        shade: view.getInt8(offset + 16),
        pal: view.getUint8(offset + 17),
        clipdist: view.getUint8(offset + 18),
        filler: view.getUint8(offset + 19),
        xrepeat: view.getUint8(offset + 20),
        yrepeat: view.getUint8(offset + 21),
        xoffset: view.getInt8(offset + 22),
        yoffset: view.getInt8(offset + 23),
        sectnum: view.getInt16(offset + 24, true),
        statnum: view.getInt16(offset + 26, true),
        ang: view.getInt16(offset + 28, true),
        owner: view.getInt16(offset + 30, true),
        xvel: view.getInt16(offset + 32, true),
        yvel: view.getInt16(offset + 34, true),
        zvel: view.getInt16(offset + 36, true),
        lotag: view.getInt16(offset + 38, true),
        hitag: view.getInt16(offset + 40, true),
        extra: view.getInt16(offset + 42, true)
      });
      offset += 44;
    }

    return {
      version,
      start: { x: startx, y: starty, z: startz, ang: startang, sector: startsector },
      numsectors,
      numwalls,
      numsprites,
      sectors,
      walls,
      sprites
    };
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const buffer = await file.arrayBuffer();
      const data = parseMapFile(buffer);
      setMapData(data);
      setError(null);
      
      // Reset view
      setZoom(1);
      setPan({ x: 0, y: 0 });
    } catch (err) {
      setError(`Error parsing map file: ${err.message}`);
      console.error(err);
    }
  };

  const drawMap = () => {
    if (!mapData || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, width, height);

    // Calculate map bounds
    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;
    
    mapData.walls.forEach(wall => {
      minX = Math.min(minX, wall.x);
      maxX = Math.max(maxX, wall.x);
      minY = Math.min(minY, wall.y);
      maxY = Math.max(maxY, wall.y);
    });

    const mapWidth = maxX - minX;
    const mapHeight = maxY - minY;
    const scale = Math.min(width / mapWidth, height / mapHeight) * 0.8 * zoom;

    // Transform function
    const transform = (x, y) => ({
      x: (x - minX) * scale + width / 2 - (mapWidth * scale) / 2 + pan.x,
      y: (y - minY) * scale + height / 2 - (mapHeight * scale) / 2 + pan.y
    });

    ctx.save();

    // Draw sectors (filled)
    mapData.sectors.forEach((sector, sectorIdx) => {
      ctx.beginPath();
      let firstPoint = true;
      
      for (let i = 0; i < sector.wallnum; i++) {
        const wallIdx = sector.wallptr + i;
        const wall = mapData.walls[wallIdx];
        const pos = transform(wall.x, wall.y);
        
        if (firstPoint) {
          ctx.moveTo(pos.x, pos.y);
          firstPoint = false;
        } else {
          ctx.lineTo(pos.x, pos.y);
        }
      }
      
      ctx.closePath();
      ctx.fillStyle = `rgba(40, 40, 60, 0.3)`;
      ctx.fill();
    });

    // Draw walls
    mapData.walls.forEach((wall, idx) => {
      const point2 = mapData.walls[wall.point2];
      if (!point2) return;

      const pos1 = transform(wall.x, wall.y);
      const pos2 = transform(point2.x, point2.y);

      ctx.beginPath();
      ctx.moveTo(pos1.x, pos1.y);
      ctx.lineTo(pos2.x, pos2.y);
      
      // Color code: red for outer walls, cyan for portals
      if (wall.nextwall === -1) {
        ctx.strokeStyle = '#ff4444';
        ctx.lineWidth = 2;
      } else {
        ctx.strokeStyle = '#44cccc';
        ctx.lineWidth = 1;
      }
      
      ctx.stroke();
    });

    // Draw sprites
    mapData.sprites.forEach((sprite, idx) => {
      const pos = transform(sprite.x, sprite.y);
      
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, 3, 0, Math.PI * 2);
      
      // Color by picnum for variety
      const hue = (sprite.picnum * 137) % 360;
      ctx.fillStyle = `hsl(${hue}, 70%, 60%)`;
      ctx.fill();
      
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      ctx.stroke();
    });

    // Draw player start position
    const startPos = transform(mapData.start.x, mapData.start.y);
    ctx.beginPath();
    ctx.arc(startPos.x, startPos.y, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#00ff00';
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw player direction indicator
    const angle = (mapData.start.ang / 2048) * Math.PI * 2;
    const dirX = startPos.x + Math.cos(angle - Math.PI / 2) * 15;
    const dirY = startPos.y + Math.sin(angle - Math.PI / 2) * 15;
    ctx.beginPath();
    ctx.moveTo(startPos.x, startPos.y);
    ctx.lineTo(dirX, dirY);
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.restore();
  };

  useEffect(() => {
    const updateCanvasSize = () => {
      if (canvasRef.current) {
        const canvas = canvasRef.current;
        const container = canvas.parentElement;
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        drawMap();
      }
    };

    updateCanvasSize();
    window.addEventListener('resize', updateCanvasSize);
    return () => window.removeEventListener('resize', updateCanvasSize);
  }, [mapData, zoom, pan]);

  const handleMouseDown = (e) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setPan({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleZoomIn = () => setZoom(z => Math.min(z * 1.5, 10));
  const handleZoomOut = () => setZoom(z => Math.max(z / 1.5, 0.1));
  const handleResetView = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  return (
    <div className="w-full h-screen bg-gray-900 text-white flex flex-col">
      {/* Header */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <h1 className="text-2xl font-bold mb-2">BUILD Engine Map Viewer</h1>
        <div className="flex items-center gap-4">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
          >
            <Upload size={20} />
            Load .MAP File
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".map"
            onChange={handleFileUpload}
            className="hidden"
          />
          
          {mapData && (
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-400">
                {mapData.numsectors} sectors / {mapData.numwalls} walls / {mapData.numsprites} sprites
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Error display */}
      {error && (
        <div className="bg-red-900 border border-red-700 p-3 m-4 rounded">
          {error}
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 relative">
        {!mapData ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-gray-400">
              <Upload size={64} className="mx-auto mb-4 opacity-50" />
              <p className="text-xl">Load a BUILD .MAP file to begin</p>
              <p className="text-sm mt-2">Supports Duke Nukem 3D and other BUILD engine maps</p>
            </div>
          </div>
        ) : (
          <>
            <canvas
              ref={canvasRef}
              width={1920}
              height={1080}
              className="w-full h-full cursor-move"
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseUp}
            />

            {/* Controls */}
            <div className="absolute top-4 right-4 flex flex-col gap-2">
              <button
                onClick={handleZoomIn}
                className="p-2 bg-gray-800 hover:bg-gray-700 rounded shadow-lg"
                title="Zoom In"
              >
                <ZoomIn size={24} />
              </button>
              <button
                onClick={handleZoomOut}
                className="p-2 bg-gray-800 hover:bg-gray-700 rounded shadow-lg"
                title="Zoom Out"
              >
                <ZoomOut size={24} />
              </button>
              <button
                onClick={handleResetView}
                className="p-2 bg-gray-800 hover:bg-gray-700 rounded shadow-lg"
                title="Reset View"
              >
                <Home size={24} />
              </button>
            </div>

            {/* Legend */}
            <div className="absolute bottom-4 left-4 bg-gray-800 bg-opacity-90 p-4 rounded shadow-lg">
              <h3 className="font-bold mb-2 flex items-center gap-2">
                <Info size={16} />
                Legend
              </h3>
              <div className="text-sm space-y-1">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-0.5 bg-red-500"></div>
                  <span>Solid walls</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-0.5 bg-cyan-400"></div>
                  <span>Portals (connections)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{background: 'hsl(180, 70%, 60%)'}}></div>
                  <span>Sprites</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  <span>Player start</span>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default BuildMapViewer;