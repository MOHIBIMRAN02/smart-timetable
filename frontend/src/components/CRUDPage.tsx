import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { Edit2, Trash2, Plus, Loader } from "lucide-react";

interface CRUDPageProps<T> {
  title: string;
  subtitle: string;
  items: T[];
  isLoading: boolean;
  columns: { key: keyof T; label: string; render?: (value: any, item: T) => React.ReactNode }[];
  onEdit?: (item: T) => void;
  onDelete?: (id: number) => void;
  onNew?: () => void;
  showActions?: boolean;
}

export default function CRUDPage<T extends { id: number }>({
  title,
  subtitle,
  items,
  isLoading,
  columns,
  onEdit,
  onDelete,
  onNew,
  showActions = true,
}: CRUDPageProps<T>) {
  if (isLoading) {
    return <div className="flex items-center justify-center h-96"><Loader className="animate-spin" /></div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="page-title">{title}</h1>
          <p className="text-slate-600 mt-1">{subtitle}</p>
        </div>
        {onNew && (
          <button className="btn-primary flex items-center gap-2" onClick={onNew}>
            <Plus size={16} /> Add New
          </button>
        )}
      </div>

      <div className="card overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200">
              {columns.map((col) => (
                <th key={String(col.key)} className="text-left py-3 px-4">
                  {col.label}
                </th>
              ))}
              {showActions && (onEdit || onDelete) && <th className="text-left py-3 px-4">Actions</th>}
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan={columns.length + (showActions ? 1 : 0)} className="text-center py-4 text-slate-500">
                  No items found
                </td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id} className="border-b border-slate-100 hover:bg-slate-50">
                  {columns.map((col) => (
                    <td key={String(col.key)} className="py-3 px-4">
                      {col.render ? col.render((item as any)[col.key], item) : String((item as any)[col.key] || "-")}
                    </td>
                  ))}
                  {showActions && (onEdit || onDelete) && (
                    <td className="py-3 px-4 flex gap-2">
                      {onEdit && (
                        <button onClick={() => onEdit(item)} className="text-blue-600 hover:text-blue-800">
                          <Edit2 size={16} />
                        </button>
                      )}
                      {onDelete && (
                        <button onClick={() => onDelete(item.id)} className="text-red-600 hover:text-red-800">
                          <Trash2 size={16} />
                        </button>
                      )}
                    </td>
                  )}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
