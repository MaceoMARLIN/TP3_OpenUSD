using UnityEngine;
using UnityEditor;
using UnityEngine.Rendering;

public class FixAllMaterials : EditorWindow
{
    [MenuItem("Tools/Fix All USD Materials")]
    public static void Fix()
    {
        string[] allAssets = AssetDatabase.FindAssets("t:Material");
        int count = 0;

        string[] transparentMats = { 
            "foliage", "foliage_001", "grass", "flower", "leaf", "blossom" 
        };

        foreach (string guid in allAssets)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            Object[] allObjects = AssetDatabase.LoadAllAssetsAtPath(path);

            foreach (Object obj in allObjects)
            {
                Material mat = obj as Material;
                if (mat == null) continue;

                string matNameLower = mat.name.ToLower();
                bool isTransparent = false;
                foreach (string t in transparentMats)
                    if (matNameLower.Contains(t)) { isTransparent = true; break; }

                // Cherche la texture par nom exact avec _baseColor
                string[] texGuids = AssetDatabase.FindAssets(
                    mat.name + "_baseColor t:Texture2D",
                    new[] { "Assets/Assets/textures" }
                );

                // Si pas trouvé, cherche par nom seul
                if (texGuids.Length == 0)
                    texGuids = AssetDatabase.FindAssets(
                        mat.name + " t:Texture2D",
                        new[] { "Assets/Assets/textures" }
                    );

                // Si toujours pas trouvé et c'est une variante foliage
                if (texGuids.Length == 0 && matNameLower.Contains("foliage"))
                    texGuids = AssetDatabase.FindAssets(
                        "foliage_baseColor t:Texture2D",
                        new[] { "Assets/Assets/textures" }
                    );

                Texture2D tex = null;
                if (texGuids.Length > 0)
                {
                    string texPath = AssetDatabase.GUIDToAssetPath(texGuids[0]);
                    tex = AssetDatabase.LoadAssetAtPath<Texture2D>(texPath);
                }

                // Applique le bon shader
                if (isTransparent)
                    mat.shader = Shader.Find("Universal Render Pipeline/Unlit");
                else
                    mat.shader = Shader.Find("Universal Render Pipeline/Lit");

                if (isTransparent)
                {
                    mat.SetFloat("_Surface", 1);
                    mat.SetFloat("_Blend", 0);
                    mat.SetFloat("_Cull", 0);
                    mat.SetFloat("_AlphaClip", 1);
                    mat.SetFloat("_Cutoff", 0.1f);
                    mat.SetOverrideTag("RenderType", "Transparent");
                    mat.EnableKeyword("_SURFACE_TYPE_TRANSPARENT");
                    mat.renderQueue = 3000;
                }
                else
                {
                    mat.SetFloat("_Surface", 0);
                    mat.SetFloat("_Cull", 2);
                }

                if (tex != null)
                {
                    mat.SetTexture("_BaseMap", tex);
                    Debug.Log($"✅ {mat.name} → {tex.name} | transparent: {isTransparent}");
                }
                else
                {
                    Debug.LogWarning($"⚠️ {mat.name} → texture NON trouvée");
                }

                EditorUtility.SetDirty(mat);
                count++;
            }
        }

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
        Debug.Log($"✔ {count} matériaux corrigés.");
    }
}