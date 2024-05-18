import bpy
import subprocess
import os

bl_info = {
    "name": "FF-MPEG Convert",
    "blender": (3, 6, 0),
    "category": "Render",
    "description": "Directly passes image sequences through FFmpeg after rendering, to give more export possibilities with video codecs and containers",
    "author": "baggiyi",
    "version": (1, 4)
}

class FFmpegPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    ffmpeg_executable: bpy.props.StringProperty(
        name="FFmpeg Executable Path",
        description="Path to the FFmpeg executable",
        default="",
        subtype='FILE_PATH'
    )
    
    ffmpeg_command: bpy.props.StringProperty(
        name="FFmpeg Command",
        description="Command arguments for FFmpeg",
        default="-y -c:v prores -profile:v 3 -pix_fmt yuv422p10le -c:a aac"
    )
    
    ffmpeg_container: bpy.props.StringProperty(
        name="FFmpeg Container",
        description="Output container format",
        default=".mov"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "ffmpeg_executable")
        layout.prop(self, "ffmpeg_command")
        layout.prop(self, "ffmpeg_container")

class FFmpeg_operator(bpy.types.Operator):
    bl_idname = "object.convert_myaddon_baggiyi"
    bl_label = "FFmpeg Converting"
    
    def execute(self, context):
        preferences = context.preferences.addons[__name__].preferences
        FFMPEG_EXE = f'"{preferences.ffmpeg_executable}"'
        FFMPEG_COMMAND = preferences.ffmpeg_command
        FFMPEG_CONTAINER = preferences.ffmpeg_container
        
        print("FFmpeg Operator did run!")

        # Function to execute before rendering
        def pre_render(scene):
            if not getattr(scene, "rendering_started", False):
                print("Rendering Started...")

        # Register pre_render function with render_init handler
        bpy.app.handlers.render_init.append(pre_render)

        # Function to execute after rendering
        def post_render(scene):
            if not getattr(scene, "rendering_completed", False):
                
                # Get current blend file info
                current_blend_file_path = bpy.data.filepath
                current_blend_file_name = os.path.basename(current_blend_file_path)
                print("Current blend file name:", current_blend_file_name)

                # Get current framerate
                current_framerate = scene.render.fps
                print("Current framerate:", current_framerate)
                blender_output_framerate = f" -framerate {current_framerate}"

                # Get current blender rendering format
                
                scene = bpy.context.scene
                current_file_format = scene.render.image_settings.file_format
                print("Current file format:", current_file_format)
                
                if current_file_format == ("PNG"):
                    print("PNG used!!!!")
                    ffmpeg_current_file_format = ("png")
                    
                if current_file_format == ("TIFF"):
                    print("TIFF used!!!!")
                    ffmpeg_current_file_format = ("tif")

                # Get current output folder
                output_path = bpy.context.scene.render.filepath
                print("Current output path:", output_path)
                blender_output_folder = f'"{output_path}%04d.{ffmpeg_current_file_format}"'
                FFMPEG_INPUT = f" -i {blender_output_folder}"

                # Define output settings
                FFMPEG_OUTPUT_NAME = current_blend_file_name.replace('.blend', '')
                FFMPEG_OUTPUT = f'"{output_path}{FFMPEG_OUTPUT_NAME}{FFMPEG_CONTAINER}"'

                # Execute FFmpeg command
                final_ffmpeg_execute_command = f"{FFMPEG_EXE} {blender_output_framerate} {FFMPEG_INPUT} {FFMPEG_COMMAND} {FFMPEG_OUTPUT}"
                try:
                    process = subprocess.Popen(final_ffmpeg_execute_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()  # Wait for the process to finish
                    print("FFmpeg command executed successfully.")
                    print("FFmpeg stdout:", stdout.decode())  # Print FFmpeg output
                    print("FFmpeg stderr:", stderr.decode())  # Print FFmpeg error output
                    
                    ### Delete image files in output directory
                    for filename in os.listdir(output_path):
                        if filename.endswith("." + ffmpeg_current_file_format):
                            os.remove(os.path.join(output_path, filename))
                            print(f"Deleted: {filename}")
                except subprocess.CalledProcessError as e:
                    print("Error executing FFmpeg command:", e)

        # Register post_render function with render_complete handler
        bpy.app.handlers.render_complete.append(post_render)

        return {'FINISHED'}


from bpy.app.handlers import persistent

@persistent
def load_handler(nonDocumentedParam1, nonDocumentedParam2): # both params always None
    bpy.ops.object.convert_myaddon_baggiyi()

bpy.app.handlers.load_post.append(load_handler)


def register():
    bpy.utils.register_class(FFmpegPreferences)
    bpy.utils.register_class(FFmpeg_operator)

def unregister():
    bpy.utils.unregister_class(FFmpegPreferences)
    bpy.utils.unregister_class(FFmpeg_operator)

if __name__ == "__main__":
    register()
