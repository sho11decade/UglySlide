#!/usr/bin/env python
"""Enhanced app.py with memory management improvements"""

# Add this section BEFORE "return jsonify(response_payload)"
# in the /api/process endpoint

memory_cleanup_code = '''
            # Explicitly clean up large objects before returning
            import gc
            logger.info("Cleaning up memory...")
            del presentation
            del design_generator
            del content_transformer
            del analyzer
            gc.collect()  # Force garbage collection
            logger.info("Memory cleaned up")
'''

print("Add the following code before 'return jsonify(response_payload)'")
print("in the /api/process endpoint:\n")
print(memory_cleanup_code)
