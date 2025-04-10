function AlignmentBar({ data }) {
    if (!data || typeof data !== 'object') return null;
    const total = data.oposisi + data.netral + data.koalisi;
  
    const getWidth = (value) => `${(value / total) * 100}%`;
  
    return (
      <div className="w-full">
        <div className="flex justify-between text-xs text-gray-600 mb-1">
          <span>Oposisi</span>
          <span>Netral</span>
          <span>Koalisi</span>
        </div>
        <div className="flex h-3 w-full rounded overflow-hidden bg-gray-200">
          <div
            className="bg-red-400"
            style={{ width: getWidth(data.oposisi) }}
          ></div>
          <div
            className="bg-gray-100"
            style={{ width: getWidth(data.netral) }}
          ></div>
          <div
            className="bg-blue-400"
            style={{ width: getWidth(data.koalisi) }}
          ></div>
        </div>
      </div>
    );
  }
  
  export default AlignmentBar;
  